import subprocess
from typing import List
from env import clsEnvData 
from enum import Enum
from Log import clsLog
from Error import clsError
import inspect

class enmUsbType(Enum):
    '''
    UsbデバイスのType
    '''

    TypeSerial = "Ser"
    '''
    USBタイプ：シリアル
    '''

    TypeCamera = "Cam"
    '''
    USBタイプ：カメラ
    '''

class clsUsbDeviceList:
    '''
    USBデバイスリストの値
    '''

    Name : str
    '''
    デバイス名(/dev/ttyUSB0など)
    '''

    Type : enmUsbType
    '''
    デバイスのType
    '''

    def __init__(self,pName:str,pType:enmUsbType):
        '''
        コンストラクタ
        '''
        self.Name = pName
        self.Type = pType

class clsUsbDevice(clsLog,clsError):
    '''
    USBのデバイス名を取得する
    '''

    EnvData: clsEnvData = None
    '''
    設定ファイル
    '''

    UsbSirialList : List[clsUsbDeviceList] = []
    '''
    Usbのシリアルケーブルのリスト
    '''

    UsbCameraList : List[clsUsbDeviceList] = []
    '''
    USBのカメラのリスト
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    def SearchUsbList(self):
        '''
        USBリストの作成
        '''

        cur = inspect.currentframe().f_code.co_name

        #
        # シリアルUSB
        #
        res = subprocess.run(['sudo ls /dev/ttyUSB*'],shell=True,executable='/bin/bash',capture_output=True, text=True)
        DevicesTmp = res.stdout.split('\n')
        Devices = []
        for DeviceTmp in DevicesTmp:
            if DeviceTmp != "":
                Devices.append(DeviceTmp)
        for Device in Devices:
            udevadm_output = subprocess.check_output(f"udevadm info --query=all --name={Device}", shell=True).decode("utf-8").split("\n")
            # デバイス情報を表示
            for line in udevadm_output:
                # シリアル通信のデバイス
                if "ID_USB_MODEL=" in line and "Serial" in line :
                    self.UsbSirialList.append(clsUsbDeviceList(Device,enmUsbType.TypeSerial))
                    self.LogOut(cur,clsLog.TYPE_LOG,f"serial:{Device}")

        #
        # カメラ
        #
        res = subprocess.run(['sudo ls /dev/video*'],shell=True,executable='/bin/bash',capture_output=True, text=True)

        DevicesTmp = res.stdout.split('\n')
        Devices = []
        for DeviceTmp in DevicesTmp:
            if DeviceTmp != "":
                Devices.append(DeviceTmp)

        for Device in Devices:
            udevadm_output = subprocess.check_output(f"v4l2-ctl --device={Device} --all", shell=True,stderr=subprocess.DEVNULL).decode("utf-8").split("\n")

            # デバイス情報を表示
            IsCheckOK1 = False
            IsCheckOK2 = False
            for line in udevadm_output:
                # カメラのデバイス
                if "Width/Height" in line and "1280/720" in line:
                    IsCheckOK1 = True
                if "Pixel Format" in line and "H264" in line:
                    IsCheckOK2 = True
                if IsCheckOK1 == True and IsCheckOK2 == True:
                    self.UsbCameraList.append(clsUsbDeviceList(Device,enmUsbType.TypeCamera))
                    self.LogOut(cur,clsLog.TYPE_LOG,f"camela:{Device}")
                    break

#clsUsbDevice().SearchUsbList()