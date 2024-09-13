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

import time
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler # type: ignore

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

class clsDB:

    '''
    環境設定ファイル
    '''
    EnvData : clsEnvData

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
            ConJyosetu = sqlite3.connect(self.EnvData.DB_JYOSETU)
            CurJyosetu = ConJyosetu.cursor()
            
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
            
            ConJyosetu.commit()

        except sqlite3.Error as e:
            self.HandleError(e)
        finally:
            if ConJyosetu:
                CurJyosetu.close()

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
                    ConJyosetu = sqlite3.connect(self.EnvData.DB_JYOSETU)
                    CurJyosetu = ConJyosetu.cursor()

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
                    
                    ConJyosetu.commit()

                except sqlite3.Error as e:
                    self.HandleError(e)
                finally:
                    if ConJyosetu:
                        CurJyosetu.close()

def Init():
    '''
    初期化処理
    '''

    #環境設定の読み込み(.envファイル)
    EnvData = clsEnvData()

class clsSendCommandFromDB(FileSystemEventHandler):
    '''
    DBに保存されたコマンドを送信する
    '''

    '''
    除雪のWebSocketクラス
    '''
    JyosetuDB : clsDB

    '''
    DBファイル更新の監視
    '''
    DbObserver : any

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
        self.DbObserver = Observer()
        self.DbObserver.schedule(self,path='.',recursive=False)
        self.DbObserver.start()

    def Stop(self):
        '''
        処理の停止
        '''
        self.DbObserver.stop()
        self.DbObserver.join()

    def on_modified(self,event):
        '''
        ファイルの変更イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            self.DbReadSendCommand()
    
    def on_created(self, event):
        '''
        ファイルの作成イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            self.DbReadSendCommand()

    def SendCommand(self,pCommand):
        '''
        実際のコマンドの送信
        '''
        print(f"Send Command: {pCommand}")

    def DbReadSendCommand(self):
        '''
        DBを読み込み、コマンドの送信を実行する
        '''
        env = self.JyosetuDB.EnvData

        try:
            errstep = "コマンドのレコードを取得"
            conn = sqlite3.connect(env.DB_JYOSETU)
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            sql = f'''
            Select * From {env.DB_TBL_COMMAND} 
            Where ExecFlag IS NULL
            Order by SUBSTR(Type,1,6),SendTime
            '''

            cursor.execute(sql)
            rows = cursor.fetchall()

            Commands = []

            #コマンドの送信
            for row in rows:

                Commands.append({
                    "Key" : row["ID"],
                    "Type" : row["Type"],
                    "Command" : row["Command"]
                })

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
                cursor.execute(sql,(1,now_time,Command["Key"]))
                conn.commit()

        except sqlite3.Error as e:
            print(f"SendCommand():ErrorStep:{errstep}:{e}")
        finally:
            if conn:
                conn.close()

class clsWebSocketJyosetu:
    '''
    除雪のWebSocketサーバー
    '''

    #除雪のDB
    JyosetuDB : clsDB

    #コマンドの送信
    SendCommand : clsSendCommandFromDB

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
        self.JyosetuDB.CreateDb()

        #コマンドの送信オブジェクト設定
        self.SendCommand = clsSendCommandFromDB(self.JyosetuDB)
        self.SendCommand.Start()

        #WebSocketサーバの開始
        start_server = await websockets.serve(self.WebSocketHandler, host, port)

        # ホスト名とIPアドレスの取得
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"WebSocket server is running on ws://{ip_address}:{port} or ws://{hostname}:{port}")

        await start_server.wait_closed()

    async def WebSocketHandler(self,websocket, path):
        
        '''
        WebSocketの処理
        '''
        try:
            async for message in websocket:

                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")

                print(f"Received message: {message}")

                jsonMsg = json.loads(message)
                self.JyosetuDB.InsertCommand(jsonMsg)

                #await websocket.send(f"Echo: {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
            self.SendCommand.Stop()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.SendCommand.Stop()
    
if __name__ == "__main__":

    WebSocketJyosetu : clsWebSocketJyosetu = clsWebSocketJyosetu()
    Init()
    Openning()
    asyncio.run(WebSocketJyosetu.Start())
