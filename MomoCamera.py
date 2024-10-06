from env import clsEnvData 
from Log import clsLog
from Error import clsError
from CommonUtil import CommonUtil
from CameraData import clsCameraData
import usbdev

from typing import List
import threading
import subprocess
import inspect
import os

class clsMomoCamera(clsLog,clsError):
    '''
    momoで使用するカメラ情報
    クライアントに渡すカメラの情報を作成する
    '''

    UsbDeviceCamera : usbdev.clsUsbDevice 
    '''
    Camera USBデバイス
    '''

    CameraDatas : List[clsCameraData] = []
    '''
    カメラ情報
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()
    
    def CreateCamelaData(self):
        '''
        カメラ情報を作成する
        '''
        thread = threading.Thread(target=self.CreateCamelaDataThred)
        thread.daemon = True
        thread.start()

    def CreateCamelaDataThred(self):
        '''
        カメラ情報を作成するスレッド
        '''

        #（ラズパイ用）USBデバイスの一覧を取得する
        self.UsbDevice = usbdev.clsUsbDevice()
        self.UsbDevice.SearchUsbList()
    
    def MomoServicesStart(self):
        '''
        momoのサービスを開始する
        '''
        cur = inspect.currentframe().f_code.co_name

        #./momo --no-audio-device --video-device %Device% --resolution QVGA test --port %PortNo% &
        MomoPortNo = self.EnvData.MOMO_PORT_NO_START
        LocalIp = CommonUtil.GetLocalIp()

        for Camera in self.UsbDevice.UsbCameraList:

            Args = self.EnvData.MOMO_CMD_ARGS
            Args = Args.replace("%Device%",Camera.Name)
            Args = Args.replace("%PortNo%",str(MomoPortNo))

            Cmd = ""
            if self.EnvData.MOMO_CMD_SUDO == "":
                Cmd = f"{self.EnvData.MOMO_PATH} {Args}"
            else:
                Cmd = f"{self.EnvData.MOMO_CMD_SUDO} {self.EnvData.MOMO_PATH} {Args}"
            self.LogOut(cur,clsLog.TYPE_LOG,f"momo command:{Cmd}")

            Cmds = []
            if self.EnvData.MOMO_CMD_SUDO != "":
                Cmds.append(self.EnvData.MOMO_CMD_SUDO)
            Cmds.append(self.EnvData.MOMO_PATH)
            Cmds.extend(Args.split())

            process = subprocess.Popen(Cmds)

            self.CameraDatas.append(clsCameraData(
                DeviceName=Camera.Name,
                PortNo=MomoPortNo,
                Codec=self.EnvData.MOMO_WS,
                ServerIp=LocalIp,
                ProcessId=process.pid
            ))

            MomoPortNo = MomoPortNo + 1
    
    def MomoServicesStop(self):
        '''
        momoサービスの停止
        '''
        cur = inspect.currentframe().f_code.co_name

        for Data in self.CameraDatas:
            try:
                os.kill(Data.ProcessId,9)
            except Exception as e:
                self.LogOut(cur,clsLog.TYPE_ERR,f"Unexpected error kill pid{Data.ProcessId}:{e}")

if __name__ == "__main__":
    MomoCamera = clsMomoCamera()
    MomoCamera.CreateCamelaDataThred()
    MomoCamera.MomoServicesStart()
    MomoCamera.MomoServicesStop()

