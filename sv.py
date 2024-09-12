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
    DB_TBL_DB_TBL_COMMAND : str = ""
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
        self.DB_JYOSETU = (f"{os.getenv('DB_JYOSETU')}_{now_time}.db")
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
                    CurJyosetu.execute(f'''
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
                    '{action['time']}'
                    '{now_time}'
                    )
                    ''')
                    
                    ConJyosetu.commit()

                except sqlite3.Error as e:
                    self.HandleError(e)
                finally:
                    if ConJyosetu:
                        CurJyosetu.close()



JyosetuDB = clsDB()

def Init():
    '''
    初期化処理
    '''

    #環境設定の読み込み(.envファイル)
    EnvData = clsEnvData()

    #DBの作成
    JyosetuDB = clsDB()
    JyosetuDB.CreateDb()

async def handler(websocket, path):
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
            JyosetuDB.InsertCommand(jsonMsg)

            #await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def main():
    '''
    メイン処理
    '''
    start_server = await websockets.serve(handler, host, port)

    # ホスト名とIPアドレスの取得
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"WebSocket server is running on ws://{ip_address}:{port} or ws://{hostname}:{port}")

    await start_server.wait_closed()

if __name__ == "__main__":
    Init()
    Openning()
    asyncio.run(main())
