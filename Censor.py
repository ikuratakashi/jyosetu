import os
import asyncio
import threading
import inspect
import time

if os.name != "nt": #Windows以外の場合
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

from datetime import datetime
from enum import Enum

from Graph import clsGraph
from env import clsEnvData
from Error import clsError
from Log import clsLog
from Db import clsDB
from SendMessageClient import clsSendMessageClient,enmSendMessageClientType

class clsCensor_Micro_Enum(Enum):
    '''
    マイクロ波センサーの定数
    ''' 
    CS_FRONT = "CS_FRONT"
    CS_LEFT = "CS_LEFT"
    CS_RIGHT = "CS_RIGHT"
    CS_BACK = "CS_BACK"

class clsCensor_Micro_Data():
    '''
    マイクロ波センサー データクラス
    '''
    vol : float = 0.0
    value : float = 0.0
    name : clsCensor_Micro_Enum

    def __init__(self,Name:clsCensor_Micro_Enum, Vol:float,Value:float):
        '''
        コンストラクタ
        '''
        self.vol = Vol
        self.value = Value
        self.name = Name

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

    CensorName : clsCensor_Micro_Enum
    '''
    センサーの名前
    '''

    IsDebug : bool = False
    '''
    デバッグフラグ
    '''

    IsShowGraph : bool = False
    '''
    グラフの表示
    '''

    def __init__(self,CensorName:clsCensor_Micro_Enum,IsShowGraph,IsDebug:bool = False):
        '''
        コンストラクタ
            CensorName : センサーの名前
            IsShowGraph : グラフの表示/非表示
            IsDebug : デバックモード
        '''
        self.EnvData = clsEnvData()
        self.CensorName = CensorName
        self.IsDebug = IsDebug
        self.IsShowGraph = IsShowGraph

    def Open(self):
        '''
        オープン
        '''
    
    def Stop(self):
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
        if self.IsDebug == True:
            self.Thred = threading.Thread(target=self.MicroThredDebug)
        else:
            self.Thred = threading.Thread(target=self.MicroThred)
        self.Thred.start()

    def MicroThredDebug(self):
        '''
        センサー受信の開始(デバッグ)
        ランダムな値を処理
        '''
        cur = inspect.currentframe().f_code.co_name
        import random

        if self.IsShowGraph == True:
            Graph = clsGraph(IsDebug=self.IsDebug,GraphName=self.CensorName.value,Label_X="time",Label_Y="value")

        # ランダムな値生成して、送信する
        while self.IsThredStop == False:
            try:

                if self.IsShowGraph == True:
                    Graph.StartGraph()

                RndVol = random.uniform(-1.1,1.1)
                RndValue = random.uniform(6,100)

                #送信
                data = clsCensor_Micro_Data(Name=self.CensorName,Vol=RndVol,Value=RndValue)
                if self.IsShowGraph == True:
                    Graph.DrawGraph(data.value)
                self.onReceive(data)
                self.LogOut(cur,self.Log.TYPE_MICRO,f"Micro Data : name={data.name},value={data.value},vol={data.vol}")
                time.sleep(0.01)

            except Exception as e:
                self.HandleError(cur,f"onReceive Core Unexpected error:{e}")

        if self.IsShowGraph == True:
            Graph.CloseGraph()
        
    def MicroThred(self):
        '''
        センサー受信の開始
        '''
        cur = inspect.currentframe().f_code.co_name

        Graph = clsGraph(IsDebug=self.IsDebug,GraphName=self.CensorName,Label_X="time",Label_Y="value")

        # I2Cバスの作成
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
        except Exception as e:
            self.HandleError(cur,f"I2C Bus Unexpected error:{e}")

        # ADS1115オブジェクトの作成
        try:
            ads = ADS.ADS1115(i2c)
            ads.gain = 8
        except Exception as e:
            self.HandleError(cur,f"ADS1115 Unexpected error:{e}")

        # チャンネル0のシングルエンド入力の作成
        chan = None
        try:
            if self.CensorName == clsCensor_Micro_Enum.CS_FRONT:
                chan = AnalogIn(ads, ADS.P0)
            elif self.CensorName == clsCensor_Micro_Enum.CS_BACK:
                chan = AnalogIn(ads, ADS.P1)
            elif self.CensorName == clsCensor_Micro_Enum.CS_LEFT:
                chan = AnalogIn(ads, ADS.P2)
            elif self.CensorName == clsCensor_Micro_Enum.CS_RIGHT:
                chan = AnalogIn(ads, ADS.P3)
        except Exception as e:
            self.HandleError(cur,f"AnalogIn Name:{self.CensorName} Unexpected error:{e}")

        # ADS1115から値を読み取り、送信する
        while self.IsThredStop == False:
            try:
                if chan == None:
                    continue
                else:
                    #信号受信の処理

                    if self.IsShowGraph == True:
                        Graph.StartGraph()
                         
                    #送信
                    data = clsCensor_Micro_Data(Name=self.CensorName,Vol=chan.voltage,Value=chan.value)
                    self.onReceive(data)

                    if self.IsShowGraph == True:
                        Graph.DrawGraph(data.value)

                    self.LogOut(cur,self.Log.TYPE_MICRO,f"Micro Data : name={data.name},value={data.value},vol={data.vol}")

                    time.sleep(0.01)

            except Exception as e:
                self.HandleError(cur,f"onReceive Core Unexpected error:{e}")
        
        # I2C終了処理
        try:
            i2c.deinit()
        except Exception as e:
            self.HandleError(cur,f"I2C Bus deinit Unexpected error:{e}")
    
        if self.IsShowGraph == True:
            Graph.CloseGraph()

    def onReceive(self,pData:clsCensor_Micro_Data):
        '''
        受信のイベント
        '''

        #マイクロ波の場合
        #以下のソースがclsCensorManagerに記載されている
        # self.Censor_Micro.onReceive = self.onCensor_Micro_Receive

        pass

class clsCensorManager(clsLog,clsError):
    '''
    センサー マネージャー
    '''

    EnvData : clsEnvData = None
    '''
    設定
    '''

    Censor_Micro : clsCensor_Micro = None
    '''
    センサー マイクロ波
    '''

    JyosetuDB : clsDB = None
    '''
    除雪DB
    '''

    SendClientMessage : any = None
    '''
    クライアントへのメッセージ送信
    '''

    IsDebug : bool = False
    '''
    デバッグフラグ
    '''

    def __init__(self,SendClientMessage:any,IsDebug:bool = False):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()
        self.SendClientMessage = SendClientMessage
        self.IsDebug = IsDebug
    
    def Start(self):
        '''
        各種センサーのスタート
        '''

        #DB関連
        self.JyosetuDB = clsDB() 
        self.JyosetuDB.CreateDb()
        self.JyosetuDB.DbOpen()

        # マイクロ波センサー 正面
        self.Censor_Micro = clsCensor_Micro(CensorName=clsCensor_Micro_Enum.CS_FRONT,
                                            IsShowGraph=self.EnvData.MICRO_GRAPTH_SHOW,
                                            IsDebug=self.IsDebug)
        self.Censor_Micro.onReceive = self.onCensor_Micro_Receive
        self.Censor_Micro.Start()

        # マイクロ波センサー 左
        '''
        self.Censor_Micro = clsCensor_Micro(CensorName=clsCensor_Micro_Enum.CS_LEFT,
                                            IsShowGraph=False,
                                            IsDebug=self.IsDebug)
        self.Censor_Micro.onReceive = self.onCensor_Micro_Receive
        self.Censor_Micro.Start()
        '''

    def Stop(self):
        '''
        各種センサーのクローズ
        '''

        #DB関連
        self.JyosetuDB.DbClose()

        # マイクロ波センサー
        self.Censor_Micro.Stop()

    def onCensor_Micro_Receive(self,pData:clsCensor_Micro_Data):
        '''
        マイクロ波センサーの信号を受信した時の処理
        '''
        cur = inspect.currentframe().f_code.co_name
        env = self.JyosetuDB.EnvData

        try:

            if pData.value > 1.0:

                Now :datetime = datetime.now()
                NowStr :str = Now.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

                message = {
                    "action":
                                [
                                    {
                                        "type":env.TYPE_AUTO_WAR,
                                        "button":"clutch_up",
                                        "value":"1",
                                        "time":NowStr,
                                    },
                                    {
                                        "type":env.TYPE_AUTO_WAR,
                                        "button":"accel_up",
                                        "value":"1",
                                        "time":NowStr,
                                    }
                                ]
                }

                async def InsertCommandLocal(message):
                    cur = inspect.currentframe().f_code.co_name
                    try:
                        await self.JyosetuDB.InsertCommand(message)
                    except Exception as e:
                        await self.HandleErrorAsync(cur,f"Unexpected error:{e}")

                async def some_async_function(message):
                    task = asyncio.create_task(InsertCommandLocal(message))
                    await task

                asyncio.run(some_async_function(message))

                # クライアント側にメッセージを送信する
                self.SendClientMessage_Micro(pData)
        
        except Exception as e:
            self.HandleError(cur,f"Unexpected error:{e}")

    def SendClientMessage_Micro(self,pData:clsCensor_Micro_Data):
        '''
        クライアントにメッセージを送信する
        '''
        message = ""
        if pData.name == clsCensor_Micro_Enum.CS_FRONT:
            message = "前方に障害物"
        elif pData.name == clsCensor_Micro_Enum.CS_BACK:
            message = "後方に障害物"
        elif pData.name == clsCensor_Micro_Enum.CS_LEFT:
            message = "左に障害物"
        elif pData.name == clsCensor_Micro_Enum.CS_RIGHT:
            message = "右に障害物"
        
        SendMessage : clsSendMessageClient = clsSendMessageClient()
        SendMessage.type = enmSendMessageClientType.MICRO

        SendMessage.message = message
        
        #sv.pyのclsWebSocketJyosetu.SendClientMessage()にリンクされている
        async def some_async_function(SendMessage):
            task = asyncio.create_task(self.SendClientMessage(SendMessage))
            await task

        asyncio.run(some_async_function(SendMessage))
    
if __name__ == "__main__":
    #当ソースを単体で実行したときに、このステップが実行されます

    async def DmmySendClientMessage(arg1):
        return True

    #デバックモードを解除する場合はIsDebugをFalseに設定する
    clsCensorManager(SendClientMessage=DmmySendClientMessage,IsDebug=False).Start()