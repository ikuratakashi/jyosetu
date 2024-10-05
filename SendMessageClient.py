from enum import Enum
import json
from typing import List
import copy
from CameraData import clsCameraData
class enmSendMessageClientType(Enum):
    '''
    クライアントにメッセージを送るときの型
    '''

    MICRO = "MICRO"
    '''
    マイクロ波センサー
    '''
    
    JYOSETU = "JYOSETU"
    '''
    除雪機
    '''
    
    VOCE = "VOICE"
    '''
    音声
    '''

    VIBE = "VIBE"
    '''
    振動
    '''

    TEXT = "TEXT"
    '''
    テキスト
    '''

    CAMELA = "CAMELA"
    '''
    カメラ
    '''

class clsSendMessageClient():
    '''
    クライアントに送信するメッセージの型
    '''

    message : str = ""
    '''
    メッセージ
    '''

    type : enmSendMessageClientType = enmSendMessageClientType.TEXT
    '''
    メッセージタイプ
    '''

    CameraDatas : List[clsCameraData] = []
    '''
    カメラデータ群
    '''

    def AddCameraData(self,CameraData:clsCameraData):
        '''
        カメラデータを追加
        '''
        self.CameraDatas.append(copy.deepcopy(CameraData))

    def ToJson(self) -> str:
        '''
        JSONへ変換
        '''

        DictData = {
            "message" : self.message,
            "type" : self.type.value
        }

        if self.type == enmSendMessageClientType.CAMELA:
            AddData = []
            for Data in self.CameraDatas:
                AddData.append({
                    "DeviceName" : Data.DeviceName,
                    "Codec" : Data.Codec,
                    "PortNo" : Data.PortNo,
                    "Protocol" : Data.Protocl
                })
            DictData["CameraDatas"] = AddData

        DictDataStr = json.dumps(DictData, ensure_ascii=False)
        return DictDataStr