from env import clsEnvData 
from Log import clsLog
from Error import clsError
from CommonUtil import CommonUtil
from CameraData import clsCameraData
import usbdev

from typing import List
import threading

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

        #./momo --no-audio-device --video-device %Device% --resolution QVGA test --port %PortNo% &
        MomoPortNo = self.EnvData.MOMO_PORT_NO_START
        LocalIp = CommonUtil.GetLocalIp()

        for Camera in self.UsbDevice.UsbCameraList:

            Cmd = self.EnvData.MOMO_CMD
            Cmd = Cmd.replace("%Device%",Camera.Name)
            Cmd = Cmd.replace("%PortNo%",MomoPortNo)

            self.CameraDatas.append(clsCameraData(
                DeviceName=Camera.Name,
                PortNo=MomoPortNo,
                Codec=self.EnvData.MOMO_WS,
                ServerIp=LocalIp
            ))

            MomoPortNo = MomoPortNo + 1

if __name__ == "__main__":
    MomoCamera = clsMomoCamera()
    MomoCamera.CreateCamelaData()
    MomoCamera.MomoServicesStart()

