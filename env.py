import sys
sys.path.append('lib')
import os
import time
from datetime import datetime,timedelta
from dotenv import load_dotenv  # type: ignore

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

    WS_PING_TNTERVAL:int = 20
    WS_PING_TIMEOUT:int = 20
    WS_LOG_COMMAND_SEND_DEVICE:int = 1

    DB_COM_BEFTIME:int = 30

    GP_NO_clutch_up_down:int = 2 

    AUTO_CL_QUANTITY:int = 5

    RS232C_DEV_SEND:str = "/ttyUSB0"
    RS232C_DEV_RECV:str = "/ttyUSB1"
    RS232C_BPS:int = 9600
    RS232C_TIMEOUT = 1

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

        #WebSocket関係
        try:
            self.WS_PING_TIMEOUT = int(os.getenv('WS_PING_INTERVAL'))
        except:
            pass
        try:
            self.WS_PING_TIMEOUT = int(os.getenv('WS_PING_TIMEOUT'))
        except:
            pass
        try:
            self.DB_COM_BEFTIME = int(os.getenv('DB_COM_BEFTIME'))
        except:
            pass
        try:
            self.WS_LOG_COMMAND_SEND_DEVICE = int(os.getenv('WS_LOG_COMMAND_SEND_DEVICE'))
        except:
            pass
        

        #GOPI関連
        try:
            self.GP_NO_clutch_up_down = int(os.getenv('GP_NO_clutch_up_down'))
        except:
            pass

        #自動クラッチ関連
        try:
            self.AUTO_CL_QUANTITY = int(os.getenv('AUTO_CL_QUANTITY'))
        except:
            pass

        #RS232C関連
        ##送信デバイス
        self.RS232C_DEV_SEND = os.getenv('RS232C_DEV_SEND')
        ##送信デバイス
        self.RS232C_DEV_RECV = os.getenv('RS232C_DEV_RECV')
        ##通信速度
        try:
            self.RS232C_BPS = int(os.getenv('RS232C_BPS'))
        except:
            pass
        ##タイムアウト
        try:
            self.RS232C_TIMEOUT = int(os.getenv('RS232C_TIMEOUT'))
        except:
            pass

