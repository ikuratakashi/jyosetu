from enum import Enum
import json
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

    def ToJson(self) -> str:
        '''
        JSONへ変換
        '''
        DictData = {
            "message" : self.message,
            "type" : self.type.value
        }
        DictDataStr = json.dumps(DictData, ensure_ascii=False)
        return DictDataStr