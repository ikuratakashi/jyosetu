from dotenv import load_dotenv
import os
from datetime import datetime,timedelta

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
    TYPE_AUTO_WAR : str = ""

    WS_PING_TNTERVAL:int = 20
    WS_PING_TIMEOUT:int = 20
    WS_LOG_COMMAND_SEND_DEVICE_STDOUT:int = 1
    WS_LOG_ETC_STDOUT:int = 1
    WS_LOG_FILE_OUT:int = 0
    WS_LOG_RS232C_STDOUT:int = 0
    WS_LOG_MICRO_STDOUT:int = 0

    DB_COM_BEFTIME:int = 30

    GP_NO_clutch_up_down:int = 2 
    GP_NO_ACT:int = 15

    AUTO_CL_QUANTITY:int = 5

    RS232C_DEV_SEND:str = "/ttyUSB0"
    RS232C_DEV_RECV:str = "/ttyUSB1"
    RS232C_BPS:int = 9600
    RS232C_TIMEOUT = 1

    MOMO_PORT_NO_START:int = 51001
    MOMO_WS:str = "ws"
    MOMO_CODEC:str = "H264"
    MOMO_CMD_ARGS:str = "--no-audio-device --video-device %Device% --resolution QVGA test --port %PortNo%"
    MOMO_PATH:str = "/home/jyosetu/jyosetu/momo/momo"
    MOMO_CMD_SUDO:str = ""

    MICRO_GRAPTH_SHOW:bool = False

    def __init__(self):
        '''
        コンストラクタ
        '''

        for key in list(os.environ.keys()):
            os.environ.pop(key, None)

        res = load_dotenv()

        now = datetime.now()
        now_time = now.strftime('%Y%m%d%H%M%S%f')[:-3]

        ######################################################################
        #基本関連
        ######################################################################
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
        self.TYPE_AUTO_WAR = os.getenv('TYPE_AUTO_WAR')

        ######################################################################
        #WebSocket関係
        ######################################################################
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
            self.WS_LOG_COMMAND_SEND_DEVICE_STDOUT = int(os.getenv('WS_LOG_COMMAND_SEND_DEVICE_STDOUT'))
        except:
            pass
        try:
            self.WS_LOG_ETC_STDOUT = int(os.getenv('WS_LOG_ETC_STDOUT'))
        except:
            pass
        try:
            self.WS_LOG_FILE_OUT = int(os.getenv('WS_LOG_FILE_OUT'))
        except:
            pass
        try:
            self.WS_LOG_STATUS_STDOUT = int(os.getenv('WS_LOG_STATUS_STDOUT'))
        except:
            pass
        try:
            self.WS_LOG_RS232C_STDOUT = int(os.getenv('WS_LOG_RS232C_STDOUT'))
        except:
            pass

        ######################################################################
        #マイクロ波センサー関連
        ######################################################################
        try:
            self.WS_LOG_MICRO_STDOUT = int(os.getenv('WS_LOG_MICRO_STDOUT'))
        except:
            pass
        try:
            if int(os.getenv('MICRO_GRAPTH_SHOW')) == 1:
                self.MICRO_GRAPTH_SHOW = True
            else:
                self.MICRO_GRAPTH_SHOW = False
        except:
            pass

        ######################################################################
        #GOPI関連
        ######################################################################
        try:
            self.GP_NO_clutch_up_down = int(os.getenv('GP_NO_clutch_up_down'))
        except:
            pass
        try:
            self.GP_NO_ACT = int(os.getenv('GP_NO_ACT'))
        except:
            pass

        ######################################################################
        #自動クラッチ関連
        ######################################################################
        try:
            self.AUTO_CL_QUANTITY = int(os.getenv('AUTO_CL_QUANTITY'))
        except:
            pass

        ######################################################################
        #RS232C関連
        ######################################################################
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

        ######################################################################
        #MOMO関連
        ######################################################################
        self.MOMO_PATH = os.getenv('MOMO_PATH')
        self.MOMO_CMD_SUDO = os.getenv('MOMO_CMD_SUDO')
        self.MOMO_CMD_ARGS = os.getenv('MOMO_CMD_ARGS')
        self.MOMO_WS = os.getenv('MOMO_WS')
        self.MOMO_CODEC = os.getenv('MOMO_CODEC')
        try:
            self.MOMO_PORT_NO_START = int(os.getenv('MOMO_PORT_NO_START'))
        except:
            pass

