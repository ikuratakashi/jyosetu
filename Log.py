import sys
sys.path.append('lib')
from colorama import init, Fore, Back, Style # type: ignore
from datetime import datetime,timedelta
from env import clsEnvData

class clsLog:
    '''
    ログ出力
    '''
    EnvData : clsEnvData
    '''
    設定ファイル
    '''

    TYPE_ERR : str = "ERROR"
    '''
    ログタイプ:Error
    '''

    TYPE_WAR : str = "WARNING"
    '''
    ログタイプ:WARNING
    '''

    TYPE_LOG : str = "LOG"
    '''
    ログタイプ:Log
    '''

    TYPE_STATUS : str = "STATUS"
    '''
    ログタイプ:ステータス
    '''

    TYPE_RS232C : str = "RS232C"
    '''
    ログタイプ:RS232C
    '''

    TYPE_SENDCOMMAND : str = "SEND_CMD"
    '''
    ログタイプ:送信コマンド
    '''

    TYPE_SENDCOMMAND_AUTO : str = "SEND_CMD_A"
    '''
    ログタイプ:送信コマンド
    '''

    TYPE_SAVECOMMAND : str = "SAVE_CMD"
    '''
    ログタイプ:受信コマンドの保存
    '''

    F_ERR:str = Fore.RED
    '''
    エラーの色
    '''

    F_WAR:str = Fore.YELLOW
    '''
    ワーニングの色
    '''
    
    F_OK:str = Fore.GREEN
    '''
    OKの色
    '''

    F_SEND_CMD:str = Fore.BLUE
    '''
    コマンドを送信した時の色
    '''

    F_SEND_A_CMD:str = f"{Fore.BLUE}{Back.LIGHTWHITE_EX}" 
    '''
    コマンドを送信した時の色（自動送信）
    '''

    F_SAVE_CMD:str = Fore.LIGHTBLUE_EX
    '''
    クライアントから受信したコマンドを保存したときの色
    '''

    F_DEF:str = ""
    '''
    デフォルト
    '''

    R:str = Style.RESET_ALL
    '''
    リセット
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    def LogOut(self,pCur:str,pType:str,pMessage:str):
        '''
        出力
        '''
        now = datetime.now()
        now_time = now.strftime('%y-%m-%d %H:%M:%S:%f')[:-3]
        PrintStr = ""

        if pType == clsLog.TYPE_ERR:
            '''
            Error
            '''
            PrintStr = f"{clsLog.F_ERR}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
            print(PrintStr)
        elif pType == clsLog.TYPE_WAR:
            '''
            ワーニング
            '''
            PrintStr = f"{clsLog.F_WAR}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
            print(PrintStr)
        elif pType == clsLog.TYPE_SENDCOMMAND:
            '''
            送信コマンド
            '''
            if self.EnvData.WS_LOG_COMMAND_SEND_DEVICE_STDOUT == 1:
                PrintStr = f"{clsLog.F_SEND_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
        elif pType == clsLog.TYPE_SENDCOMMAND_AUTO:
            '''
            送信コマンド自動
            '''
            if self.EnvData.WS_LOG_COMMAND_SEND_DEVICE_STDOUT == 1:
                PrintStr = f"{clsLog.F_SEND_A_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
        elif pType == clsLog.TYPE_SAVECOMMAND:
            '''
            コマンド保存
            '''
            if self.EnvData.WS_LOG_ETC_STDOUT == 1:
                PrintStr = f"{clsLog.F_SAVE_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
        elif pType == clsLog.TYPE_STATUS:
            '''
            ステータス
            '''
            if self.EnvData.WS_LOG_STATUS_STDOUT == 1:
                PrintStr = f"{clsLog.F_DEF}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
        elif pType == clsLog.TYPE_RS232C:
            '''
            RS232Cのログ
            '''
            if self.EnvData.WS_LOG_RS232C_STDOUT == 1:
                PrintStr = f"{clsLog.F_DEF}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
        else:
            '''
            通常ログ
            '''
            if self.EnvData.WS_LOG_ETC_STDOUT == 1:
                PrintStr = f"{clsLog.F_DEF}[{now_time}:{pType}:{pCur}(?)] {pMessage}{clsLog.R}"
                print(PrintStr)
