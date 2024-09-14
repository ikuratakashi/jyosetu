version = "10.2.101"
PgName = "Jyosetu Message Server"

import sys
sys.path.append('lib')
import asyncio
import websockets  # type: ignore
import socket
import os
import platform
from datetime import datetime
from dotenv import load_dotenv  # type: ignore
import sqlite3
import json
from enum import Enum
import time
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler # type: ignore
import threading
from typing import List
import signal

port = 50001
host = "0.0.0.0"  # すべてのインターフェースから接続を受け入れる

def Openning():
    '''
    オープニング
    '''
    print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
    print('')
    print(f'{PgName}')
    print('')
    print(f'var:{version}')
    print('')
    print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
    print('')
    print('')
    print(f'Wellcome to {PgName}.')
    print('')
    print('')
class clsEnvData:
    '''
    環境設定ファイルを取得する
    '''

    VERSION : str = ""
    DB_JYOSETU : str = ""
    DB_JYOSETU_MODE : str = ""
    DB_TBL_COMMAND : str = ""
    TYPE_EMERGENCY : str = ""
    TYPE_OPERATION : str = ""
    TYPE_SOUND : str = ""
    TYPE_AUTO : str = ""

    def __init__(self):
        '''
        コンストラクタ
        '''

        load_dotenv()

        now = datetime.now()
        now_time = now.strftime('%Y%m%d%H%M%S%f')[:-3]

        self.VERSION = os.getenv('VERSION')
        self.DB_JYOSETU_MODE = os.getenv('DB_JYOSETU_MODE')
        if self.DB_JYOSETU_MODE == "ONE":
            self.DB_JYOSETU = f"{os.getenv('DB_JYOSETU')}.db"
        else:
            self.DB_JYOSETU = f"{os.getenv('DB_JYOSETU')}_{now_time}.db"
        self.DB_TBL_COMMAND = os.getenv('DB_TBL_COMMAND')

        self.TYPE_EMERGENCY = os.getenv('TYPE_EMERGENCY')
        self.TYPE_OPERATION = os.getenv('TYPE_OPERATION')
        self.TYPE_SOUND = os.getenv('TYPE_SOUND')
        self.TYPE_AUTO = os.getenv('TYPE_AUTO')

class clsDB:

    EnvData : clsEnvData
    '''
    環境設定ファイル
    '''

    ConJyosetu:sqlite3.Connection = None
    '''
    除雪DBコネクション
    '''

    IsJyosetuDbOpen:bool = False
    '''
    除雪DBオープンしているか
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    def HandleError(self,pE):
        '''
        エラー処理
        '''
        print(f"{pE}")

    def IsCommandType(self,pMessage) -> bool:
        '''
        メッセージがコマンドかどうか
        '''
        result = False

        if self.EnvData.TYPE_EMERGENCY == pMessage['type']:
            result = True
        elif self.EnvData.TYPE_OPERATION == pMessage['type']:
            result = True
        elif self.EnvData.TYPE_SOUND == pMessage['type']:
            result = True

        return result


    def CreateDb(self):
        '''
        DBの作成
        '''
        try:
            CurJyosetu = self.ConJyosetu.cursor()
            
            #テーブル作成SQL
            CurJyosetu.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.EnvData.DB_TBL_COMMAND} 
            (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Type TEXT ,
            Command TEXT ,
            Quantity INTEGER ,
            SendTime TEXT ,
            RecTime TEXT ,
            ExecFlag INTEGER ,
            ExecDate TEXT )''')
            
            self.ConJyosetu.commit()

        except sqlite3.Error as e:
            self.HandleError(e)

    def DbOpen(self):
        '''
        DBをオープンする
        '''
        try:
            if self.IsJyosetuDbOpen == False:
                self.ConJyosetu = sqlite3.connect(self.EnvData.DB_JYOSETU,check_same_thread=False)
                self.IsJyosetuDbOpen = True
        except sqlite3.Error as e :
            self.HandleError(e)
            self.IsJyosetuDbOpen = False

    def DbClose(self):
        '''
        DBをクローズする
        '''
        try:
            if self.ConJyosetu != None and self.IsJyosetuDbOpen == True:
                self.ConJyosetu.close()
                self.IsJyosetuDbOpen = False
        except sqlite3.Error as e :
            self.HandleError(e)

    def InsertCommand(self,pMessage):
        '''
        コマンドを追加する
        '''

        '''
        送信されてくるjsonの形式は、

        reactのソース\\utils\\UtilsJson.js

        に定義されている
        '''

        #コマンドのタイプ
        for action in pMessage['action']:

            if self.IsCommandType(action) == True:

                now = datetime.now()
                now_time = now.strftime('%Y-%m-%d %H:%M:%S%f')[:-3]

                try:
                    CurJyosetu = self.ConJyosetu.cursor()

                    #テーブル作成SQL
                    sql = f'''
                    INSERT INTO {self.EnvData.DB_TBL_COMMAND} 
                    (
                    Type ,
                    Command ,
                    Quantity ,
                    SendTime,
                    RecTime
                    )
                    VALUES
                    (
                    '{action['type']}',
                    '{action['button']}',
                    {action['value']},
                    '{action['time']}',
                    '{now_time}'
                    )
                    '''
                    CurJyosetu.execute(sql)
                    self.ConJyosetu.commit()

                except sqlite3.Error as e:
                    self.HandleError(e)

def Init():
    '''
    初期化処理
    '''

    #環境設定の読み込み(.envファイル)
    EnvData = clsEnvData()

class clsSendCommandData():
    '''
    コマンド送信のデータ
    '''
    Key : str
    Type : str
    Command : str

    def __init__(self, pKey:str,pType:str,pCommand:str):
        '''
        コンストラクタ
        '''
        self.Key = pKey
        self.Type = pType
        self.Command = pCommand

class enmAutoClutchActionType(Enum):
    '''
    自動クラッチアップの実行タイプ
    ''' 
    STOP = 0
    START = 1

class clsSendCommandFromDB(FileSystemEventHandler):
    '''
    DBに保存されたコマンドを送信する
    '''

    JyosetuDB : clsDB = None
    '''
    除雪のWebSocketクラス
    '''

    DbObserver : any
    '''
    DBファイル更新の監視
    '''

    CommandSendCheckThred : threading.Thread = None
    '''
    コマンドを送信したかどうかの監視スレッド
    '''

    IsCommandSendCheckThredEnd : bool = False
    '''
    コマンドを送信したかどうかの監視スレッドの終了フラグ
    '''

    AutoClutchThred : threading.Thread = None
    '''
    自動クラッチアップのスレッド
    '''

    IsAutoClutchThredEnd : bool = False
    '''
    自動クラッチアップの終了フラグ
    '''

    IsAutoClutchThredEndStart : bool = None
    '''
    自動クラッチアップの終了フラグ 開始フラグ
    '''

    BefCluchDownTime : datetime = None
    '''
    前回送信したクラッチダウンの日時
    '''

    BefCommandSendTime : datetime = None
    '''
    前回送信したコマンドの日時
    '''

    IsClutchDownPressed : bool = False
    '''
    クラッチダウンを長押し中
    '''

    def __init__(self,pDb:clsDB):
        '''
        コンストラクタ
        '''
        super().__init__()
        self.JyosetuDB = pDb    

    def Start(self):
        '''
        処理開始
        '''

        #DBファイルの更新の監視を行う処理を開始
        self.DbObserver = Observer()
        self.DbObserver.schedule(self,path='.',recursive=False)
        self.DbObserver.start()

        #自動クラッチアップの開始
        self.AutoClutchSendCommandStartStop(pActionType=enmAutoClutchActionType.START)

        #一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッドを開始
        self.StartAutoClutchUpIfIdleStartThred()

    def Stop(self):
        '''
        処理の停止
        '''
        self.DbObserver.stop()
        self.DbObserver.join()

        self.IsCommandSendCheckThredEnd = True
        self.CommandSendCheckThred.join()

        self.AutoClutchSendCommandStartStop(pActionType=enmAutoClutchActionType.STOP)

    def on_modified(self,event):
        '''
        ファイルの変更イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            #コマンド送信
            Commands : List[clsSendCommandData] = self.DbReadSendCommand()
            #自動クラッチアップの実行を判定
            self.AutoClutchShouldStartStop(Commands)
            #コマンドを送信した日時を保存
            if len(Commands) > 0 :
                self.BefCommandSendTime = datetime.now()

    def on_created(self, event):
        '''
        ファイルの作成イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            #コマンド送信
            Commands : List[clsSendCommandData] = self.DbReadSendCommand()
            #自動クラッチアップの実行を判定
            self.AutoClutchShouldStartStop(Commands)
            #コマンドを送信した日時を保存
            if len(Commands) > 0 :
                self.BefCommandSendTime = datetime.now()
    
    def AutoClutchShouldStartStop(self,pCommands:List[clsSendCommandData]):
        '''
        自動クラッチアップの実行を判定
        '''
        Now : datetime = datetime.now()
        IsClutchDown : bool = False
        sec : float = 0.0
        IsStart : bool = False

        if self.BefCluchDownTime == None:
            self.BefCluchDownTime = Now

        for Command in pCommands:
            if Command.Command == "clutch_dw":
                #自動クラッチアップ ストップ
                self.AutoClutchSendCommandStartStop(pActionType=enmAutoClutchActionType.STOP)
                IsClutchDown = True
                break

        if IsClutchDown == True:

            if self.BefCluchDownTime == None:
                self.BefCluchDownTime = Now

            sec = (Now - self.BefCluchDownTime).total_seconds()
            if sec > 2 :
                IsStart = True
            self.BefCluchDownTime = Now
        
        if IsStart :
            #自動クラッチアップ 開始
            if self.IsAutoClutchThredEnd == True:
                self.AutoClutchSendCommandStartStop(pActionType=enmAutoClutchActionType.START)
    
    def StartAutoClutchUpIfIdleStartThred(self):
        '''
        一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッドを起動する
        '''
        self.CommandSendCheckThred = threading.Thread(target=self.StartAutoClutchUpIfIdle)
        self.CommandSendCheckThred.start()

    def StartAutoClutchUpIfIdle(self):
        '''
        一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する
        '''
        while not self.IsCommandSendCheckThredEnd:
            
            Now :datetime = datetime.now()
            sec : float = 0.0
            IsStart : bool = False

            if self.BefCommandSendTime == None:
                self.BefCommandSendTime = Now
            
            sec = (Now - self.BefCommandSendTime).total_seconds()
            if sec > 2 :
                IsStart = True

            if IsStart :
                #自動クラッチアップ 開始
                self.AutoClutchSendCommandStartStop(pActionType=enmAutoClutchActionType.START)

    def SendCommand(self,pCommand:clsSendCommandData):
        '''
        実際のコマンドの送信
        '''
        env = self.JyosetuDB.EnvData
        if pCommand.Type != env.TYPE_AUTO:
            print(f"Send Command: Key={pCommand.Key},Type={pCommand.Type},Command={pCommand.Command}")

    def DbReadSendCommand(self) -> List[clsSendCommandData]:
        '''
        DBを読み込み、コマンドの送信を実行する

        戻り値：
            Commans -> List[clsSendCommandData] : 送信したコマンド
        '''
        env = self.JyosetuDB.EnvData
        Commands:List[clsSendCommandData] = []

        try:
            errstep = "コマンドのレコードを取得"

            conn : sqlite3.Connection = self.JyosetuDB.ConJyosetu
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            sql = f'''
            Select * From {env.DB_TBL_COMMAND} 
            Where ExecFlag IS NULL
            Order by SUBSTR(Type,1,6),SendTime
            '''

            cursor.execute(sql)
            rows = cursor.fetchall()

            #コマンドの送信
            for row in rows:

                Commands.append(
                    clsSendCommandData(
                        pKey = row["ID"],
                        pType = row["Type"],
                        pCommand = row["Command"]
                    )
                )

                #送信
                errstep = "コマンドを送信"
                self.SendCommand(Commands[len(Commands)-1])
            
            #送信したコマンドを送信完了にする
            errstep = "コマンドを送信完了にする"
            for Command in Commands:

                now = datetime.now()
                now_time = now.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

                sql = f'''
                Update 
                    {env.DB_TBL_COMMAND}
                Set
                    ExecFlag = ?,
                    ExecDate = ?
                Where
                    ID = ?
                '''
                cursor.execute(sql,(1,now_time,Command.Key))
                conn.commit()

        except sqlite3.Error as e:
            print(f"SendCommand():ErrorStep:{errstep}:{e}")

        return Commands

    def AutoClutchSendCommandStartStop(self,pActionType:enmAutoClutchActionType):
        '''
        クラッチのコマンドを送り続ける 停止／再開

        パラメータ:
            pEnabled (bool): 挨拶する相手の名前
        '''
        if pActionType == enmAutoClutchActionType.START:

            self.BefCluchDownTime = None

            #if self.AutoClutchThred == None or self.AutoClutchThred.is_alive() == False:
            if self.IsAutoClutchThredEndStart == None or self.IsAutoClutchThredEnd == True:
                self.IsAutoClutchThredEndStart = False
                self.IsAutoClutchThredEnd = False
                self.AutoClutchThred = threading.Thread(target=self.AutoClutchSendCommand)
                self.AutoClutchThred.start()
        else:
            if self.AutoClutchThred != None:
                self.IsAutoClutchThredEndStart = True
                self.AutoClutchThred.join()
                self.AutoClutchThred = None
                self.IsAutoClutchThredEnd = True

    def AutoClutchSendCommand(self):
        '''
        クラッチのコマンドを送り続ける コマンド送信
        '''
        SendCommand : clsSendCommandData = clsSendCommandData(pKey=-1,pType=self.JyosetuDB.EnvData.TYPE_AUTO,pCommand="clutch_up")
        while not self.IsAutoClutchThredEndStart:
            self.SendCommand(SendCommand)
            #time.sleep(0.25)
    
class clsWebSocketJyosetu:
    '''
    除雪のWebSocketサーバー
    '''

    JyosetuDB : clsDB
    #除雪のDB

    SendCommand : clsSendCommandFromDB
    #コマンドの送信

    WebSocketServer : websockets.serve
    #WebSocketsサーバー

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    async def Start(self):
        '''
        サーバの開始
        '''
        #DBの作成
        self.JyosetuDB = clsDB() 
        self.JyosetuDB.DbOpen()
        self.JyosetuDB.CreateDb()

        #コマンドの送信オブジェクト設定
        self.SendCommand = clsSendCommandFromDB(self.JyosetuDB)
        self.SendCommand.Start()

        #WebSocketサーバの開始
        self.WebSocketServer = await websockets.serve(self.WebSocketHandler, host, port)

        # ホスト名とIPアドレスの取得
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"WebSocket server is running on ws://{ip_address}:{port} or ws://{hostname}:{port}")

        await self.WebSocketServer.wait_closed()

    async def close_server(self,server):
        '''
        サーバーの終了
        '''
        server.close()
        await server.wait_closed()

    async def WebSocketHandler(self,websocket, path):
        
        '''
        WebSocketの処理
        '''
        try:
            async for message in websocket:

                '''
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                '''

                #print(f"Received message: {message}")

                jsonMsg = json.loads(message)
                self.JyosetuDB.InsertCommand(jsonMsg)

                #await websocket.send(f"Echo: {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
            self.RunExit()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.RunExit()

    def signal_handler(self,sig,frame):
        '''
        プログラムの終了時
        '''
        self.RunExit()
    
    def RunExit(self):
        '''
        終了処理
        '''
        self.JyosetuDB.DbClose()
        self.SendCommand.Stop()
        #self.WebSocketServer.close()

def shutdown():
    '''
    プログラムの終了時
    '''
    WebSocketJyosetu.RunExit()
    print("Server ShatDown...")
    sys.exit(0)

if __name__ == "__main__":

    #プログラム終了時のハンドリング
    signal.signal(signal.SIGINT,lambda sig, frame: shutdown())

    WebSocketJyosetu : clsWebSocketJyosetu = clsWebSocketJyosetu()
    Init()
    Openning()
    try:
        asyncio.run(WebSocketJyosetu.Start())
    except KeyboardInterrupt:
        print("\nServer stopped by user")