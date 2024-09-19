version = "10.2.101"
PgName = "Jyosetu Message Server"

import sys
sys.path.append('lib')
import asyncio
import websockets  # type: ignore
import socket
import os
import platform
from datetime import datetime,timedelta
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
import inspect
from colorama import init, Fore, Back, Style # type: ignore
import queue
import RPi.GPIO as GPIO
import subprocess
import pigpio
import copy

port = 50001
host = "0.0.0.0"  # すべてのインターフェースから接続を受け入れる
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
        if pType == self.TYPE_WAR:
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

class clsError:
    '''
    エラー処理
    '''

    Log : clsLog = clsLog()
    '''
    ログ
    '''

    def HandleError(self,pCur,pMessage):
        '''
        エラー処理
        '''
        self.Log.LogOut(pCur=pCur,pType=clsLog.TYPE_ERR,pMessage=pMessage)


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
    WS_PING_TNTERVAL:int = 20
    WS_PING_TIMEOUT:int = 20
    DB_COM_BEFTIME:int = 30

    GP_NO_clutch_up_down:int = 2 


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

        #GOPI関連
        try:
            self.GP_NO_clutch_up_down = int(os.getenv('GP_NO_clutch_up_down'))
        except:
            pass

class clsDB(clsLog,clsError):

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
        cur = inspect.currentframe().f_code.co_name
        try:
            self.DbOpen()

            CurJyosetu = self.ConJyosetu.cursor()
            CurJyosetu.execute('BEGIN TRANSACTION')

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
            self.HandleError(cur,e)
            self.DbRollBack()
        finally:
            self.DbClose()

    def DbOpen(self):
        '''
        DBをオープンする
        '''
        cur = inspect.currentframe().f_code.co_name
        try:
            if self.IsJyosetuDbOpen == False:
                self.ConJyosetu = sqlite3.connect(self.EnvData.DB_JYOSETU,check_same_thread=False)
                self.IsJyosetuDbOpen = True
        except sqlite3.Error as e :
            self.HandleError(cur,e)
            self.IsJyosetuDbOpen = False

    def DbClose(self):
        '''
        DBをクローズする
        '''
        cur = inspect.currentframe().f_code.co_name
        try:
            if self.ConJyosetu != None and self.IsJyosetuDbOpen == True:
                self.ConJyosetu.close()
                self.IsJyosetuDbOpen = False
        except sqlite3.Error as e :
            self.HandleError(cur,e)

    def DbRollBack(self):
        '''
        DBのロールバック
        '''
        cur = inspect.currentframe().f_code.co_name
        try:
            self.ConJyosetu.rollback()
        except sqlite3.Error as e :
            self.HandleError(cur,e)

    async def InsertCommand(self,pMessage):
        '''
        コマンドを追加する
        '''
        cur = inspect.currentframe().f_code.co_name

        '''
        送信されてくるjsonの形式は、

        reactのソース\\utils\\UtilsJson.js

        に定義されている
        '''

        #コマンドのタイプ
        try:

            CurJyosetu = self.ConJyosetu.cursor()
            CurJyosetu.execute('PRAGMA busy_timeout = 5000') 

            IsInsert : bool = False

            for action in pMessage['action']:

                if self.IsCommandType(action) == True:

                    now = datetime.now()
                    now_time = now.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

                    try:

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
                        IsInsert = True

                        sec="??"
                        try:
                            RecTime = datetime.strptime(action['time'], "%Y/%m/%d %H:%M:%S:%f")
                            sec = (now - RecTime).total_seconds()
                        except:
                            pass

                        self.LogOut(cur,clsLog.TYPE_SAVECOMMAND,f"Type={action['type']},Command={action['button']},Value={action['value']},{Back.GREEN}sec={sec}{Style.RESET_ALL}{clsLog.F_SAVE_CMD},SendTime:{action['time']},RecTime:{now_time}")

                    except sqlite3.Error as e:
                        self.HandleError(cur,e)

            if IsInsert :
                #トランザクションを開始していない場合は、Commitは必要ないらしい
                self.ConJyosetu.commit()
                pass

        except sqlite3.Error as e:
            self.HandleError(cur,e)
        finally:
            pass

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
    Quantity : str

    def __init__(self, pKey:str,pType:str,pCommand:str,pQuantity:str):
        '''
        コンストラクタ
        '''
        self.Key = pKey
        self.Type = pType
        self.Command = pCommand
        self.Quantity = pQuantity

class enmAutoClutchActionType(Enum):
    '''
    自動クラッチアップの実行タイプ
    ''' 
    STOP = 0
    START = 1

class clsCommandSendQueueValue():
    '''
    CommandSendにかかわる値で、スレッド間で共有する値
    '''
    BefCommandSendTime : datetime = None
    '''
    前回コマンドを送信した日時
    '''
    BefCluchDownTime : datetime = None
    '''
    前回CluchDownコマンドを送信した日時
    '''

class clsAutoClutchSendCommandQueueValue():
    IsAutoClutchThredEnd : bool = False
    '''
    自動クラッチアップの終了フラグ 開始フラグ
    '''
    IsAutoClutchThredRunning : bool = False
    '''
    自動クラッチアップの実行中かどうかのフラグ
    '''

class clsCommandToGPIO(clsLog):
    '''
    コマンドをGOIPへ送る
    '''
    
    EnvData : clsEnvData
    '''
    環境設定ファイル
    '''

    pwm_clutch_up_down = None
    '''
    クラッチのアップとダウン
    '''

    clutch_angle = 0
    '''
    クラッチの角度
    '''

    pi : pigpio.pi
    '''
    PGIO
    '''

    CmdClutchQues : List[clsSendCommandData] = []
    '''
    クラッチのキュー
    '''

    IsCommandSendClutchThredStop : bool = False
    '''
    スレッドの実行をストップするフラグ
    '''

    CommandSendClutchThred : threading.Thread = None
    '''
    クラッチコマンドを送信するスレッド
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()
        self.pi = pigpio.pi()
        pass

    def Stop(self):
        '''
        スレッドを停止する
        '''
        self.CommandSendClutchThredStop()

    def CommandSendClutchThredStart(self):
        '''
        クラッチのスレッドを開始する
        '''
        self.IsCommandSendClutchThredStop == False
        if self.CommandSendClutchThred == None:
            self.CommandSendClutchThred = threading.Thread(target=self.SendCommandClutch)
            self.CommandSendClutchThred.start()

    def CommandSendClutchThredStop(self):
        '''
        クラッチのスレッドを止める
        '''
        self.IsCommandSendClutchThredStop = True
        if self.CommandSendClutchThred != None:
            self.CommandSendClutchThred.join()
            self.CommandSendClutchThred = None

    def SendCommandClutch(self):
        '''
        クラッチのスレッドを開始する
        '''
        while self.IsCommandSendClutchThredStop == False:

            while self.CmdClutchQues:

                Cmd : clsSendCommandData = self.CmdClutchQues.pop()

                if Cmd.Command == "clutch_up":
                    self.Clutch_UP(Cmd)
                    pass
                elif Cmd.Command == "clutch_dw":
                    self.Clutch_DOWN(Cmd)
                    pass
                else:
                    pass

    
    def Send(self,pCmd:clsSendCommandData):
        '''
        コマンドをデバイスに送信する
        '''

        # クラッチの情報送信用のスレッドを開始
        self.CommandSendClutchThredStart()

        if pCmd.Command == "clutch_up":
            # キューへコマンドを追加
            self.CmdClutchQues.append(copy.deepcopy(pCmd))
        elif pCmd.Command == "clutch_dw":
            # キューへコマンドを追加
            self.CmdClutchQues.append(copy.deepcopy(pCmd))
        else:
            pass

    def ServoSetAngle(self,angle,pIsStart:bool = False):
        '''
        サーボモータの角度の設定
        '''
        cur = inspect.currentframe().f_code.co_name

        pulse_width = (angle / 180) * (2500 - 500) + 500
        if self.pi.connected == True:
            self.pi.set_servo_pulsewidth(self.EnvData.GP_NO_clutch_up_down,pulse_width)
        else:
            self.LogOut(cur,clsLog.TYPE_WAR,f"pigpiodのサーバが起動していないためサーボモーターを制御できません。sudo pigpiod でデーモンを起動してください。")

    def Clutch_UP(self,pCmd:clsSendCommandData):
        '''
        クラッチ アップ
        '''
        e = self.EnvData
        cnt = 0
        max = pCmd.Quantity

        self.ServoSetAngle(self.clutch_angle,True)

        while True:
            cnt += 1
            if cnt > max:
                break
            self.clutch_angle += 10
            if self.clutch_angle <= 180:
                self.ServoSetAngle(self.clutch_angle)
                #print(self.clutch_angle)
                #time.sleep(0.3)
                pass
            else:
                self.clutch_angle = 180
                break

    def Clutch_DOWN(self,pCmd:clsSendCommandData):
        '''
        クラッチ ダウン
        '''
        e = self.EnvData
        cnt = 0
        max = pCmd.Quantity

        self.ServoSetAngle(self.clutch_angle,True)

        while True:
            cnt += 1
            if cnt > max:
                break
            self.clutch_angle -= 10
            if self.clutch_angle >= 0:
                self.ServoSetAngle(self.clutch_angle)
                #print(self.clutch_angle)
                #time.sleep(0.3)
                pass
            else:
                self.clutch_angle = 0
                break

class clsSendCommandFromDB(FileSystemEventHandler,clsLog,clsError):
    '''
    DBに保存されたコマンドを送信する
    '''

    JyosetuDB : clsDB = None
    '''
    除雪のWebSocketクラス
    '''

    DbObserver : Observer = None # type: ignore
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

    IsAutoClutchThredEnd : bool = None
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

    IsDbUpdate : bool = False
    '''
    DBの更新中
    '''

    CommandSendThred : threading.Thread = None
    '''
    DBの更新チェックスレッド
    '''

    IsCommandSendEnd : bool = False
    '''
    DBの更新チェックスレッドの終了フラグ
    '''

    CommandSendQueue : queue.Queue = None
    '''
    キュー
    '''

    AutoClutchSendCommandQueue : queue.Queue = None
    '''
    キュー
    '''

    CommandSendQueueValue : clsCommandSendQueueValue = clsCommandSendQueueValue()
    '''
    CommandSendにかかわる値で、スレッド間で共有する値
    '''
    
    AutoClutchSendCommandQueueValue : clsAutoClutchSendCommandQueueValue = clsAutoClutchSendCommandQueueValue()
    '''
    AutoClutchSendCommandにかかわる値で、スレッド間で共有する値
    '''

    CommandToDevice : clsCommandToGPIO
    '''
    コマンドをデバイスに送信
    '''

    def __init__(self,pDb:clsDB):
        '''
        コンストラクタ
        '''
        super().__init__()
        self.JyosetuDB = pDb
        self.CommandToDevice = clsCommandToGPIO()
        #self.CommandSendQueue = queue.Queue()
        #self.AutoClutchSendCommandQueue = queue.Queue()

    def Start(self):
        '''
        処理開始
        '''

        #DBファイルの更新の監視を行う処理を開始
        #self.DbObserver = Observer()
        #self.DbObserver.schedule(self,path='.',recursive=False)
        #self.DbObserver.start()

        #自動クラッチアップのスレッド開始
        self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.START)
        #一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッドを開始
        self.StartAutoClutchUpIfIdleThreadStart()
        #コマンド送信のスレッド開始
        self.CommandSendThredStart()

    def Stop(self):
        '''
        処理の停止
        '''
        #self.DbObserver.stop()
        #self.DbObserver.join()

        #自動クラッチアップのスレッド終了
        self.StartAutoClutchUpIfIdleThreadEnd()
        #一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッド終了
        self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.STOP)
        #コマンド送信のスレッド開始
        self.CommandSendThredEnd()
        #コマンド送信関連のスレッドの停止
        self.CommandToDevice.Stop()

    def on_modified(self,event):
        '''
        ファイルの変更イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            #コマンドの送信
            if self.IsDbUpdate == False:
                self.CommandSendDaemon()

    def on_created(self, event):
        '''
        ファイルの作成イベント
        '''
        if os.path.basename(event.src_path) == self.JyosetuDB.EnvData.DB_JYOSETU:
            #コマンドの送信
            if self.IsDbUpdate == False:
                self.CommandSendDaemon()

    def CommandSendRun(self):
        '''
        DBチェックのスレッド
        '''
        while self.IsCommandSendEnd == False:

            #self.CommandSendQueueValue = self.CommandSendQueue.get()

            #
            #if self.CommandSendQueueValue.BefCluchDownTime == None:
            #    self.CommandSendQueueValue.BefCluchDownTime = datetime.now()
            #
            #if self.CommandSendQueueValue.BefCommandSendTime == None:
            #    self.CommandSendQueueValue.BefCommandSendTime = datetime.now()
            #

            # コマンドの送信
            self.CommandSend()

            #self.CommandSendQueue.put(self.CommandSendQueueValue)
            #self.CommandSendQueue.task_done()
            time.sleep(1)

    def CommandSendThredStart(self):
        '''
        DBチェックのスレッドスタート
        '''
        self.IsCommandSendEnd = False
        self.CommandSendThred = threading.Thread(target=self.CommandSendRun)
        self.CommandSendThred.start()

        #self.CommandSendQueue.put(self.CommandSendQueueValue)

    def CommandSendThredEnd(self):
        '''
        DBチェックのスレッド終了
        '''
        if self.CommandSendThred != None:
            self.IsCommandSendEnd = True
            self.CommandSendThred.join()

    def CommandSendDaemon(self):
        '''
        コマンド送信のデーモン起動
        '''
        thread = threading.Thread(target=self.CommandSend)
        thread.daemon = True
        thread.start()
    
    def CommandSend(self):
        '''
        コマンドの送信
        '''
        #コマンド送信
        Commands : List[clsSendCommandData] = self.DbReadSendCommand()
        #自動クラッチアップの実行を判定
        self.AutoClutchShouldStartStop(Commands)
        #コマンドを送信した日時を保存
        if len(Commands) > 0 :
            self.CommandSendQueueValue.BefCommandSendTime = datetime.now()

    def AutoClutchShouldStartStop(self,pCommands:List[clsSendCommandData]):
        '''
        自動クラッチアップの実行を判定
        '''
        cur = inspect.currentframe().f_code.co_name
        Now : datetime = datetime.now()
        IsClutchDown : bool = False
        sec : float = 0.0
        IsStart : bool = False

        for Command in pCommands:
            if Command.Command == "clutch_dw":
                #自動クラッチアップ ストップ
                self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.STOP)
                IsClutchDown = True
                break

        if IsClutchDown == True:

            if self.CommandSendQueueValue.BefCluchDownTime == None:
                self.CommandSendQueueValue.BefCluchDownTime = Now

            sec = (Now - self.CommandSendQueueValue.BefCluchDownTime).total_seconds()

            self.LogOut(cur,clsLog.TYPE_LOG,f"前回のclutch_dw送信から {sec}秒 ")

            if sec > 4 :
                IsStart = True

            self.CommandSendQueueValue.BefCluchDownTime = Now
        
        if IsStart :
            #自動クラッチアップ 開始
            #self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.START)
            pass
    
    def StartAutoClutchUpIfIdleThreadStart(self):
        '''
        一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッドを起動する
        '''
        self.IsCommandSendCheckThredEnd = False
        self.CommandSendCheckThred = threading.Thread(target=self.StartAutoClutchUpIfIdle)
        self.CommandSendCheckThred.start()

    def StartAutoClutchUpIfIdleThreadEnd(self):
        '''
        一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する をチェックするためのスレッドを終了する
        '''
        if self.CommandSendCheckThred != None:
            self.IsCommandSendCheckThredEnd = True
            self.CommandSendCheckThred.join()

    def StartAutoClutchUpIfIdle(self):
        '''
        一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する
        '''
        cur = inspect.currentframe().f_code.co_name
        while self.IsCommandSendCheckThredEnd == False:
            
            Now :datetime = datetime.now()
            sec : float = 0.0
            IsStart : bool = False

            if self.CommandSendQueueValue.BefCommandSendTime != None:
                sec = (Now - self.CommandSendQueueValue.BefCommandSendTime).total_seconds()
                #self.LogOut(cur,clsLog.TYPE_LOG,f"前回の何かしらのボタンダウン送信から {sec}秒 ")
                if sec > 2 :
                    IsStart = True

                if IsStart :
                    #自動クラッチアップ 開始
                    self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.START)
                    self.CommandSendQueueValue.BefCommandSendTime = None
                    pass

    def SendCommand(self,pCommand:clsSendCommandData):
        '''
        実際のコマンドの送信
        '''
        cur = inspect.currentframe().f_code.co_name
        env = self.JyosetuDB.EnvData
        if pCommand.Type == env.TYPE_AUTO:
            self.LogOut(cur,clsLog.TYPE_SENDCOMMAND_AUTO,f"Key={pCommand.Key},Type={pCommand.Type},Command={pCommand.Command},Quantity={pCommand.Quantity}")
        else:
            self.LogOut(cur,clsLog.TYPE_SENDCOMMAND,f"Key={pCommand.Key},Type={pCommand.Type},Command={pCommand.Command},Quantity={pCommand.Quantity}")

        self.CommandToDevice.Send(pCommand)

        #thread = threading.Thread(target=self.CommandToDevice.Send,args=(pCommand,))
        #thread.daemon = True
        #thread.start()

    def DbReadSendCommand(self) -> List[clsSendCommandData]:
        '''
        DBを読み込み、コマンドの送信を実行する

        戻り値：
            Commans -> List[clsSendCommandData] : 送信したコマンド
        '''

        cur = inspect.currentframe().f_code.co_name
        env = self.JyosetuDB.EnvData
        Commands:List[clsSendCommandData] = []

        if self.IsDbUpdate == True:
            return Commands
        
        self.IsDbUpdate = True

        DB : clsDB = clsDB()

        try:
            errstep = "コマンドのレコードを取得"

            DB.DbOpen()

            conn : sqlite3.Connection = DB.ConJyosetu
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            WhereTimeDateTime = datetime.now() - timedelta(seconds=env.DB_COM_BEFTIME)
            WhereTime = WhereTimeDateTime.strftime('%Y-%m-%d %H:%M:%S.%f')

            sql = f'''
            Select * From {env.DB_TBL_COMMAND} 
            Where ExecFlag IS NULL and SendTime >= '{WhereTime}'
            Order by SUBSTR(Type,1,6),SendTime
            '''

            cursor.execute(sql)
            rows = cursor.fetchall()

            #コマンドの送信
            cursor.execute('BEGIN TRANSACTION')
            for row in rows:

                #送信コマンドの更新
                errstep = "コマンドを送信完了にする"
                now = datetime.now()
                RecTime = now
                try:
                    RecTime = datetime.strptime(row["RecTime"], "%Y-%m-%d %H:%M:%S:%f")
                    sec = (now - RecTime).total_seconds()
                    self.LogOut(cur,clsLog.TYPE_LOG,f"now({now})-RecTime({RecTime}) = {sec}")
                except:
                    pass

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

                cursor.execute('PRAGMA busy_timeout = 10000')
                cursor.execute(sql,(1,now_time,row["ID"]))

                Commands.append(
                    clsSendCommandData(
                        pKey = row["ID"],
                        pType = row["Type"],
                        pCommand = row["Command"],
                        pQuantity = row["Quantity"]
                    )
                )

            conn.commit()

            #送信
            errstep = "コマンドを送信"
            for Command in Commands:
                self.SendCommand(Command)
            
            #送信したコマンドを送信完了にする
            if False:
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
            self.HandleError(cur,f"{errstep}:{e}")
            DB.DbRollBack()
        finally:
            DB.DbClose()

        self.IsDbUpdate = False

        return Commands

    def AutoClutchSendCommandThreadStartStop(self,pActionType:enmAutoClutchActionType):
        '''
        クラッチのコマンドを送り続ける 停止／再開

        パラメータ:
            pEnabled (bool): 挨拶する相手の名前
        '''
        if pActionType == enmAutoClutchActionType.START:
            if self.AutoClutchSendCommandQueueValue.IsAutoClutchThredRunning == False:
                self.AutoClutchSendCommandQueueValue.IsAutoClutchThredEnd = False
                self.AutoClutchSendCommandQueueValue.IsAutoClutchThredRunning = True
                self.AutoClutchThred = threading.Thread(target=self.AutoClutchSendCommand)
                self.AutoClutchThred.start()
        else:
            if self.AutoClutchThred != None and self.AutoClutchSendCommandQueueValue.IsAutoClutchThredRunning == True:
                self.AutoClutchSendCommandQueueValue.IsAutoClutchThredEnd = True
                try:
                    self.AutoClutchThred.join()
                except Exception as e:
                    pass
                self.AutoClutchThred = None
                self.AutoClutchSendCommandQueueValue.IsAutoClutchThredRunning = False

    def AutoClutchSendCommand(self):
        '''
        クラッチのコマンドを送り続ける コマンド送信
        '''
        SendCommand : clsSendCommandData = clsSendCommandData(pKey=-1,pType=self.JyosetuDB.EnvData.TYPE_AUTO,pCommand="clutch_up",pQuantity=5)
        while self.AutoClutchSendCommandQueueValue.IsAutoClutchThredEnd == False:
            self.SendCommand(SendCommand)
            time.sleep(1.0)
    
class clsWebSocketJyosetu(clsLog,clsError):
    '''
    除雪のWebSocketサーバー
    '''

    JyosetuDB : clsDB = None
    '''
    除雪のDB
    '''

    SendCommand : clsSendCommandFromDB = None
    '''
    コマンドの送信
    '''

    WebSocketServer : websockets.serve
    '''
    WebSocketsサーバー
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()

    def HandleError(self,pCur,pE):
        '''
        エラー処理
        '''
        self.LogOut(pCur,clsLog.TYPE_ERR,pE)

    async def Start(self):
        '''
        サーバの開始
        '''
        cur = inspect.currentframe().f_code.co_name

        #pigpioのデーモンを起動
        subprocess.Popen(['sudo','pigpiod'])

        time.sleep(2)

        #DBの作成
        self.JyosetuDB = clsDB() 
        self.JyosetuDB.CreateDb()

        #共通で使用するDBをオープンする
        self.JyosetuDB.DbOpen()

        #コマンドの送信オブジェクト設定
        self.SendCommand = clsSendCommandFromDB(self.JyosetuDB)
        self.SendCommand.Start()

        #WebSocketサーバの開始
        self.WebSocketServer = await websockets.serve(self.WebSocketHandler, 
                                                      host, 
                                                      port,
                                                      ping_interval=self.EnvData.WS_PING_TNTERVAL,
                                                      ping_timeout=self.EnvData.WS_PING_TIMEOUT)

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

    async def process_message(self,message):
        # メッセージの処理
        print(f"Processing message: {message}")

    async def WebSocketHandler(self,websocket, path):
        '''
        WebSocketの処理
        '''
        cur = inspect.currentframe().f_code.co_name
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
                #self.InsertCommandDaemon(jsonMsg)
                asyncio.create_task(self.JyosetuDB.InsertCommand(jsonMsg))
                
                #await websocket.send(f"Echo: {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            self.HandleError(cur,e)
            #self.RunExit()
        except Exception as e:
            self.HandleError(cur,e)
            #self.RunExit()

    def InsertCommandDaemon(self,pJsonMsg):
        '''
        コマンドのDBへの書き込みデーモン
        '''
        thread = threading.Thread(target=self.JyosetuDB.InsertCommand,args=(pJsonMsg,))
        thread.daemon = True
        thread.start()

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