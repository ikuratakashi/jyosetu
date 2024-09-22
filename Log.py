import sys
sys.path.append('lib')
from colorama import init, Fore, Back, Style # type: ignore
from datetime import datetime,timedelta

class clsLog:
    '''
    ログ出力
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

    def LogOut(self,pCur:str,pType:str,pMessage:str):
        '''
        出力
        '''
        now = datetime.now()
        now_time = now.strftime('%y-%m-%d %H:%M:%S:%f')[:-3]

        if pType == self.TYPE_ERR:
            '''
            Error
            '''
            print(f"{self.F_ERR}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")
        elif pType == self.TYPE_WAR:
            '''
            ワーニング
            '''
            print(f"{self.F_WAR}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")

        elif pType == self.TYPE_SENDCOMMAND:
            '''
            送信コマンド
            '''
            print(f"{self.F_SEND_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")
        elif pType == self.TYPE_SENDCOMMAND_AUTO:
            '''
            送信コマンド自動
            '''
            print(f"{self.F_SEND_A_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")
        elif pType == self.TYPE_SAVECOMMAND:
            '''
            コマンド保存
            '''
            print(f"{self.F_SAVE_CMD}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")
        else:
            '''
            通常ログ
            '''
            print(f"{self.F_DEF}[{now_time}:{pType}:{pCur}(?)] {pMessage}{self.R}")
