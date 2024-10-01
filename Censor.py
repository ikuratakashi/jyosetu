import threading
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

    Thred : threading.Thread = None
    '''
    処理のスレッド
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
        self.IsThredStop = True
        if self.Thred != None:
            self.Thred.join()
            self.Thred = None

    def Start(self):
        '''
        クラッチコマンドを送信するスレッド
        '''
        self.Thred = threading.Thread(target=self.MicroThred)
        self.Thred.start()

    def MicroThred(self):
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

class clsCensorManager(clsLog,clsError):
    '''
    センサー マネージャー
    '''

    EnvData : clsEnvData = None
    '''
    設定
    '''

    IsThredStop : bool = False
    '''
    スレッドの終了フラグ
    '''

    Censor_Micro : clsCensor_Micro = None
    '''
    センサー マイクロ波
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()
    
    def Start(self):
        '''
        各種センサーのスタート
        '''

        # マイクロ波センサー
        self.Censor_Micro = clsCensor_Micro()
        self.Censor_Micro.start()