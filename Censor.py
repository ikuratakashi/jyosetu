from env import clsEnvData
from Error import clsError
from Log import clsLog
import inspect

class clsCensor_Micro(clsLog,clsError):
    '''
    マイクロ波センサー クラス
    '''

    EnvData : clsEnvData = None
    '''
    設定
    '''

    IsThredStop : bool = False
    '''
    スレッドの終了フラグ
    '''

    Log : clsLog = clsLog()
    '''
    ログ
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    def open(self):
        '''
        オープン
        '''
    
    def close(self):
        '''
        クローズ
        '''

    def start(self):
        '''
        センサー受信の開始
        '''
        cur = inspect.currentframe().f_code.co_name
        while self.IsThredStop == False:
            try:

                #信号受信の処理
                data = ""
                self.onReceive(data)
            except Exception as e:
                self.HandleError(cur,f"Unexpected error:{e}")
    
    def onReceive(self,pData):
        '''
        受信のイベント
        '''
        pass
