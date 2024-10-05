#!/home/jyosetu/.pyenv/shims/python

version = "10.2.101"
PgName = "Jyosetu Message Server"

'''
■良く使う処理

[メソッド名を取得してログを出力する （ローカル版）]
[...メソッドを再起呼び出しで実行するとselfが変わってしまうので、そういう場合はこれを使う]

cur = inspect.currentframe().f_code.co_name
Log = clsLog()
Log.LogOut(cur,clsLog.TYPE_STATUS,f"Server ShatDown Start...")

[メソッド名を取得してログを出力する （各クラス内での実行版）]

self.LogOut(cur,clsLog.TYPE_ERR,f"Serial error:{e}")
self.LogOut(cur,clsLog.TYPE_WAR,f"CommandSend Serial Re Open Device:{Back.WHITE} {Device.Name} {Back.RESET}")
self.LogOut(cur,clsLog.TYPE_LOG,f"前回のclutch_dw送信から {sec}秒 ")
self.LogOut(cur,clsLog.TYPE_STATUS,f"Serial Open Device:{Back.GREEN}{SelDev}{Back.RESET}")
self.LogOut(cur,clsLog.TYPE_SENDCOMMAND_AUTO,f"Key={pCommand.Key},Type={pCommand.Type},Command={pCommand.Command},Quantity={pCommand.Quantity}")
self.LogOut(cur,clsLog.TYPE_SENDCOMMAND,f"Key={pCommand.Key},Type={pCommand.Type},Command={pCommand.Command},Quantity={pCommand.Quantity}")
'''

'''
■ 各処理へのショートカット文字
※この文字で検索するとそこへ飛ぶ

[クラス関連]
ラズパイのACT LEDの点滅
コマンド送信のデータ
CommandSendにかかわる値で、スレッド間で共有する値
自動クラッチのコマンド送信のスレッド内で共有する値
コマンドをGOIPへ送る

[重要クラス]
DBクラス
コマンドをRS232Cで送る
DBに保存されたコマンドを送信する
除雪のWebSocketサーバー

[メソッド関連]
自動クラッチダウンの有効と開始を設定
DBの作成
コマンドをテーブルに追加する
DBに保存されたコマンドを送信する 処理開始
DBに保存されたコマンドを送信する 処理の停止
一定の間、コマンドを送信していない場合は、自動クラッチアップを開始する
クラッチのコマンドを送り続ける 停止／再開
RS232C シリアル通信を開く

[重要メソッド]
コマンドをデバイスに送信
DBを読み込み、コマンドの送信を実行する
プログラムの終了時
RS232C コマンドをデバイスへ送信する
RS232C クラッチのスレッドを開始する
RS232C クラッチのコマンドを送信する
RS232C クラッチ アップ コマンド送信
RS232C クラッチ ダウン コマンド送信

[変数]
RS232C USBデバイス

[ラズパイ独自の処理など]
（ラズパイ用）ACTランプの点滅 初期化
（ラズパイ用）USBデバイスの一覧を取得する

[処理関連]
自動クラッチダウンの有効と開始を設定

[その他]
オープニング
送られてきたコマンドをすぐに処理したい場合は、ここへ記述

[画面のコマンドを増やした時に修正する場所]
RS232C コマンドをデバイスに送信する
自動クラッチダウンの有効と開始を設定

'''

import sys

import asyncio
import gpiod.line_info
import websockets 
from websockets.server import WebSocketServerProtocol
import socket
import platform
from datetime import datetime,timedelta
from dotenv import load_dotenv
import sqlite3
import json
from enum import Enum
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from typing import List
import signal
import inspect
import queue
import subprocess
import copy

from env import clsEnvData 
from Log import clsLog
from Error import clsError
from Censor import clsCensorManager

import usbdev

import pigpio
import serial
from colorama import Back, Style
from Db import clsDB
from env import clsEnvData
import subprocess

from SendMessageClient import clsSendMessageClient,enmSendMessageClientType
import RPi.GPIO as GPIO
import gpiod
import gpiozero

port = 50001
host = "0.0.0.0"  # すべてのインターフェースから接続を受け入れる

class clsActLed():
    '''
    ラズパイのACT LEDの点滅
    '''

    EnvData : clsEnvData = None
    '''
    Envデータ
    '''

    LedOnOff : bool = False
    '''
    LEDの点灯/消灯状態
    '''

    GPIOLineAct : gpiod.LineRequest
    '''
    ACTランプとして使用するGPIOのライン
    '''

    def Init(self):
        '''
        デフォルトの点灯を無効に
        '''

        self.EnvData = clsEnvData()

        # GPIOラインの設定
        LINE = self.EnvData.GP_NO_ACT
        gpiod.Chip('/dev/gpiochip0').close()
        self.GPIOLineAct = gpiod.request_lines(
            '/dev/gpiochip0',
            consumer="LED",
            config={
                LINE : gpiod.LineSettings(
                    direction=gpiod.line.Direction.OUTPUT,
                    output_value=gpiod.line.Value.INACTIVE
                )
            })

        #os.system('sudo sh -c echo none > /sys/class/leds/ACT/trigger')
        os.system('echo none | sudo tee /sys/class/leds/ACT/trigger >/dev/null 2>&1')

    def On(self):
        '''
        点灯
        '''
        #os.system('sudo sh -c echo 1 > /sys/class/leds/ACT/brightness')
        self.GPIOLineAct.set_value(self.EnvData.GP_NO_ACT,gpiod.line.Value.ACTIVE)
        os.system('echo 1 | sudo tee /sys/class/leds/ACT/brightness >/dev/null 2>&1')
        self.LedOnOff = True
        
    def Off(self):
        '''
        消灯
        '''
        self.GPIOLineAct.set_value(self.EnvData.GP_NO_ACT,gpiod.line.Value.INACTIVE)
        #os.system('sudo sh -c echo 0 > /sys/class/leds/ACT/brightness')
        os.system('echo 0 | sudo tee /sys/class/leds/ACT/brightness >/dev/null 2>&1')
        self.LedOnOff = False
    
    def AutoOnOff(self):
        '''
        自動点灯／消灯
        '''
        thread = threading.Thread(target=self.AutoOnOffThred)
        thread.daemon = True
        thread.start()

    def AutoOnOffThred(self):
        '''
        自動点灯／消灯 スレッド
        '''
        self.On()
        time.sleep(0.1)
        self.Off()

    def Stop(self):
        '''
        終了処理
        '''
        chip = gpiod.Chip('/dev/gpiochip0')
        if chip != None:
            chip.close()

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
    '''
    自動クラッチのコマンド送信のスレッド内で共有する値
    '''
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

class clsCommandToRS232C(clsLog,clsError):
    '''
    コマンドをRS232Cで送る
    '''
    
    EnvData : clsEnvData
    '''
    環境設定ファイル
    '''

    UsbDevice : usbdev.clsUsbDevice 
    '''
    RS232C USBデバイス
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

    CmmandSendSerial : serial.Serial = None
    '''
    コマンドを送るシリアルポート
    '''

    ActLed : clsActLed = clsActLed()
    '''
    ACT LEDの点灯／消灯
    '''

    def __init__(self):
        '''
        コンストラクタ
        '''

        #（ラズパイ用）ACTランプの点滅 初期化
        self.EnvData = clsEnvData()
        self.ActLed : clsActLed = clsActLed()
        self.ActLed.Init()

        #（ラズパイ用）USBデバイスの一覧を取得する
        self.UsbDevice = usbdev.clsUsbDevice()
        self.UsbDevice.SearchUsbList()

        self.SerialOpen()


    def SerialOpen(self,pDev:str = "") -> bool:
        '''
        RS232C シリアル通信を開く
        戻り値：オープンの成功:True／失敗:False
        '''
        cur = inspect.currentframe().f_code.co_name
        e = self.EnvData
        IsError = False
        Result = True
        SelDev = "none"
        if pDev == "" and len(self.UsbDevice.UsbSirialList) > 0:
            SelDev = self.UsbDevice.UsbSirialList[0].Name
        else:
            SelDev = pDev

        if SelDev == "":
            self.LogOut(cur,clsLog.TYPE_STATUS,f"Serial No Device:'{SelDev}'")
        else:
            try:
                self.CmmandSendSerial = serial.Serial(SelDev, e.RS232C_BPS, timeout=e.RS232C_TIMEOUT,xonxoff=True)
                self.LogOut(cur,clsLog.TYPE_STATUS,f"Serial Open Device:{Back.GREEN}{SelDev}{Back.RESET}")
            except serial.SerialException as e:
                self.LogOut(cur,clsLog.TYPE_ERR,f"Serial error:{e}")
                IsError = True
            except Exception as e:
                self.LogOut(cur,clsLog.TYPE_ERR,f"Unexpected error:{e}")
                IsError = True

        if IsError == True:
            Result = False
            if pDev == "":
                for Device in self.UsbDevice.UsbSirialList:
                    IsOpen = self.SerialOpen(Device.Name)
                    if IsOpen == True:
                        Result = True
                        self.LogOut(cur,clsLog.TYPE_ERR,f"CommandSend Serial No Open Device:{Back.YELLOW} {Device.Name} {Back.RESET}")
                        self.LogOut(cur,clsLog.TYPE_WAR,f"CommandSend Serial Re Open Device:{Back.WHITE} {Device.Name} {Back.RESET}")
                        break
        
        return Result

    def Stop(self):
        '''
        スレッドを停止する
        '''
        cur = inspect.currentframe().f_code.co_name
        self.CommandSendClutchThredStop()
        try:
            if self.CmmandSendSerial != None:
                self.CmmandSendSerial.close()
        except Exception as e:
            self.HandleError(cur,f"{e}")
        
        self.ActLed.Stop()

    def CommandSendClutchThredStart(self):
        '''
        RS232C クラッチのスレッドを開始する
        '''
        self.IsCommandSendClutchThredStop == False
        if self.CommandSendClutchThred == None:
            self.CommandSendClutchThred = threading.Thread(target=self.SendCommandClutch)
            self.CommandSendClutchThred.start()

    def CommandSendClutchThredStop(self):
        '''
        RS232C クラッチのスレッドを止める
        '''
        self.IsCommandSendClutchThredStop = True
        if self.CommandSendClutchThred != None:
            self.CommandSendClutchThred.join()
            self.CommandSendClutchThred = None

    def SendCommandClutch(self):
        '''
        RS232C クラッチのコマンドを送信する
        '''
        while self.IsCommandSendClutchThredStop == False:

            while self.CmdClutchQues:

                if self.IsCommandSendClutchThredStop == True:
                    break

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
        RS232C コマンドをデバイスに送信する
        '''
        QueSizeMax = 1
        if len(self.CmdClutchQues) >= QueSizeMax:
            self.CmdClutchQues.pop(0)

        # クラッチの情報送信用のスレッドを開始
        self.CommandSendClutchThredStart()

        if pCmd.Command == "clutch_up":
            # キューへコマンドを追加
            self.CmdClutchQues.append(copy.deepcopy(pCmd))
        elif pCmd.Command == "clutch_dw":
            # キューへコマンドを追加
            self.CmdClutchQues.append(copy.deepcopy(pCmd))
        elif pCmd.Command == "accel_up":
            #アクセル アップ
            self.SendDevice("a_up",pCmd.Quantity)
        elif pCmd.Command == "accel_dw":
            #アクセル ダウン
            self.SendDevice("a_dw",pCmd.Quantity)
        elif pCmd.Command == "move_fw":
            #移動 前進
            self.SendDevice("m_fw")
        elif pCmd.Command == "move_bk":
            #移動 後進
            self.SendDevice("m_bk",pCmd.Quantity)
        elif pCmd.Command == "move_right":
            #移動 右
            self.SendDevice("m_r",pCmd.Quantity)
        elif pCmd.Command == "move_left":
            #移動 左
            self.SendDevice("m_l",pCmd.Quantity)
        elif pCmd.Command == "chute_L_lup":
            #雪射出口 左上向き
            self.SendDevice("c_L_lup",pCmd.Quantity)
        elif pCmd.Command == "chute_L_up":
            #雪射出口 上向き
            self.SendDevice("c_L_up",pCmd.Quantity)
        elif pCmd.Command == "chute_L_rup":
            #雪射出口 右上向き
            self.SendDevice("c_L_rup",pCmd.Quantity)
        elif pCmd.Command == "chute_L_right":
            #雪射出口 右向き
            self.SendDevice("c_L_right",pCmd.Quantity)
        elif pCmd.Command == "chute_L_rdw":
            #雪射出口 右下向き
            self.SendDevice("c_L_rdw",pCmd.Quantity)
        elif pCmd.Command == "chute_L_dw":
            #雪射出口 下向き
            self.SendDevice("c_L_dw",pCmd.Quantity)
        elif pCmd.Command == "chute_L_ldw":
            #雪射出口 左下向き
            self.SendDevice("c_L_ldw",pCmd.Quantity)
        elif pCmd.Command == "chute_L_left":
            #雪射出口 左向き
            self.SendDevice("c_L_left",pCmd.Quantity)
        elif pCmd.Command == "chute_R_lup":
            #雪射出口 スティック右 左上向き
            self.SendDevice("c_R_lup",pCmd.Quantity)
        elif pCmd.Command == "chute_R_up":
            #雪射出口 上向き
            self.SendDevice("c_R_up",pCmd.Quantity)
        elif pCmd.Command == "chute_R_rup":
            #雪射出口 右上向き
            self.SendDevice("c_R_rup",pCmd.Quantity)
        elif pCmd.Command == "chute_R_right":
            #雪射出口 右向き
            self.SendDevice("c_R_right",pCmd.Quantity)
        elif pCmd.Command == "chute_R_rdw":
            #雪射出口 右下向き
            self.SendDevice("c_R_rdw",pCmd.Quantity)
        elif pCmd.Command == "chute_R_dw":
            #雪射出口 下向き
            self.SendDevice("c_R_dw",pCmd.Quantity)
        elif pCmd.Command == "chute_R_ldw":
            #雪射出口 左下向き
            self.SendDevice("c_R_ldw",pCmd.Quantity)
        elif pCmd.Command == "chute_R_left":
            #雪射出口 左向き
            self.SendDevice("c_R_left",pCmd.Quantity)
        elif pCmd.Command == "btn_sankaku":
            #未設定ボタン△
            self.SendDevice("btn_sankaku")
        elif pCmd.Command == "btn_sikaku":
            #未設定ボタン□
            self.SendDevice("btn_sikaku")
        elif pCmd.Command == "btn_on":
            #歯の回転のON
            self.SendDevice("on")
        elif pCmd.Command == "btn_off":
            #歯の回転のOFF
            self.SendDevice("off",5)
        elif pCmd.Command == "btn_em":
            #緊急停止
            self.SendDevice("em",5)
        else:
            pass
    
    def SendDevice(self,pCmd:str,pCnt:int = 1):
        '''
        RS232C コマンドをデバイスへ送信する
        '''
        cur = inspect.currentframe().f_code.co_name
        try:

            # 一時的
            self.ActLed.AutoOnOff()

            Cmds = []
            max = pCnt
            for i in range(max):
                Cmds.append(pCmd)

            if self.CmmandSendSerial == None :
                self.SerialOpen()

            if self.CmmandSendSerial != None :

                if self.CmmandSendSerial.is_open == False:
                    self.CmmandSendSerial.open()

                if self.CmmandSendSerial.is_open == True:

                    self.ActLed.AutoOnOff()
                    self.CmmandSendSerial.write(f"{','.join(Cmds)},".encode('utf-8'))

                else:
                    self.LogOut(cur,clsLog.TYPE_WAR,f"Serial Closed Device:{self.EnvData.RS232C_DEV_SEND}")

        except Exception as e:
            self.LogOut(cur,clsLog.TYPE_WAR,f"Serial Closed Device:{self.EnvData.RS232C_DEV_SEND}")
            self.HandleError(cur,f"{e}")
            self.SerialOpen()

    def Clutch_UP(self,pCmd:clsSendCommandData):
        '''
        RS232C クラッチ アップ コマンド送信
        '''
        e = self.EnvData
        cnt = 0
        max = pCmd.Quantity

        while True:

            if self.IsCommandSendClutchThredStop == True:
                break

            cmdQues = []

            for i in range(15):
                if cnt > max:
                    break
                cnt += 1
                cmdQues.append("c_up")

            self.SendDevice(",".join(cmdQues))
            if cnt > max:
                break
            time.sleep(1.5)

    def Clutch_DOWN(self,pCmd:clsSendCommandData):
        '''
        RS232C クラッチ ダウン コマンド送信
        '''
        e = self.EnvData
        cnt = 0
        max = pCmd.Quantity

        while True:

            if self.IsCommandSendClutchThredStop == True:
                break

            cmdQues = []

            for i in range(15):
                if cnt > max:
                    break
                cnt += 1
                cmdQues.append("c_dw")

            self.SendDevice(",".join(cmdQues))
            if cnt > max:
                break
            time.sleep(1.5)

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

    #CommandToDevice : clsCommandToGPIO
    CommandToDevice : clsCommandToRS232C
    '''
    コマンドをデバイスに送信
    '''

    IsAutoClutchDwRun : bool = True
    '''
    自動クラッチダウンの実行フラグ
    '''

    def __init__(self,pDb:clsDB):
        '''
        コンストラクタ
        '''
        super().__init__()
        self.JyosetuDB = pDb
        #self.CommandToDevice = clsCommandToGPIO()
        self.CommandToDevice = clsCommandToRS232C()
        #self.CommandSendQueue = queue.Queue()
        #self.AutoClutchSendCommandQueue = queue.Queue()

    def Start(self):
        '''
        DBに保存されたコマンドを送信する 処理開始
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
    
    def SetAutoClutchDwFlag(self,pValue:bool=True):
        '''
        自動クラッチダウンのフラグを設定する
        引数：
            pValue - 設定するフラグ True:実行／False:停止
        '''
        self.IsAutoClutchDwRun = pValue

    def Stop(self):
        '''
        DBに保存されたコマンドを送信する 処理の停止
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
        self.LogOut("Stop",clsLog.F_DEF,"self.CommandToDevice.Stop() Start")
        self.CommandToDevice.Stop()
        self.LogOut("Stop",clsLog.F_DEF,"self.CommandToDevice.Stop() End")

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
                self.LogOut(cur,clsLog.TYPE_LOG,f"前回の何かしらのボタンダウン送信から {sec}秒 ")
                if sec > 2 :
                    IsStart = True

                if IsStart :
                    #自動クラッチアップ 開始
                    self.AutoClutchSendCommandThreadStartStop(pActionType=enmAutoClutchActionType.START)
                    self.CommandSendQueueValue.BefCommandSendTime = None
                    pass

    def SendCommand(self,pCommand:clsSendCommandData):
        '''
        コマンドをデバイスに送信
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

                ##########################################################
                # 送られてきたコマンドをすぐに処理したい場合は、ここへ記述
                ##########################################################

                #自動クラッチダウンの有効と開始を設定
                if Command.Command == "auto_clutch_dw_on":
                    #有効
                    self.SetAutoClutchDwFlag(True)
                elif Command.Command == "auto_clutch_dw_off":
                    #無効
                    self.SetAutoClutchDwFlag(False)
            
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
        SendCommand : clsSendCommandData = clsSendCommandData(pKey=-1,pType=self.JyosetuDB.EnvData.TYPE_AUTO,pCommand="clutch_up",pQuantity=self.JyosetuDB.EnvData.AUTO_CL_QUANTITY)
        while self.AutoClutchSendCommandQueueValue.IsAutoClutchThredEnd == False:
            if self.IsAutoClutchDwRun == True:
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

    ConnectedClients = set()
    '''
    接続してきたクライアント
    '''

    Websocket : WebSocketServerProtocol = None
    '''
    WebSocket
    '''

    CensorManager : clsCensorManager = None
    '''
    センサーマネージャー
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
        #subprocess.Popen(['sudo','pigpiod'])

        time.sleep(2)

        #DBの作成
        self.JyosetuDB = clsDB() 
        self.JyosetuDB.CreateDb()

        #センサーマネージャー
        self.CensorManager = clsCensorManager(self.SendClientMessage)
        self.CensorManager.Start()

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
        print("")
        self.LogOut(cur,clsLog.TYPE_STATUS,f"WebSocket server is running on {Back.GREEN}ws://{ip_address}:{port}{Back.RESET} or {Back.GREEN}ws://{hostname}:{port}{Back.RESET}")

        await self.WebSocketServer.wait_closed()

    async def close_server(self,server):
        '''
        サーバーの終了
        '''
        server.close()
        await server.wait_closed()

    async def WebSocketHandler(self,websocket:WebSocketServerProtocol, path):
        '''
        WebSocketの処理
        '''
        cur = inspect.currentframe().f_code.co_name
        self.ConnectedClients.add(websocket)

        try:
            async for message in websocket:
                '''
                クライアントから送らて来たメッセージを受信する所
                '''

                '''
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                '''

                #print(f"Received message: {message}")
                self.LogOut(cur,self.Log.TYPE_LOG,f"Client Receive Message:{message}")
                jsonMsg = json.loads(message)
                asyncio.create_task(self.JyosetuDB.InsertCommand(jsonMsg))
                #await websocket.send(f"Echo: {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            self.HandleError(cur,e)
        except Exception as e:
            self.HandleError(cur,e)

    async def SendClientMessage(self,Message:clsSendMessageClient):
        '''
        クライアントへメッセージを送信する
        '''
        cur = inspect.currentframe().f_code.co_name
        MessageStr = Message.ToJson()

        try:

            if self.ConnectedClients:
                for client in self.ConnectedClients:
                    if client.open:
                        await client.send(MessageStr)
                    else:
                        self.LogOut(cur,clsLog.TYPE_WAR,f"WebSocket Closed No SendMessage {MessageStr}")

        except websockets.exceptions.ConnectionClosedError as e:
            self.HandleError(cur,e)
        except Exception as e:
            self.HandleError(cur,e)


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
        self.CensorManager.Stop()
        #self.WebSocketServer.close()

def shutdown():
    '''
    プログラムの終了時
    '''
    cur = inspect.currentframe().f_code.co_name
    Log = clsLog()
    Log.LogOut(cur,clsLog.TYPE_STATUS,f"Server ShatDown Start...")
    WebSocketJyosetu.RunExit()
    Log.LogOut(cur,clsLog.TYPE_STATUS,f"Server ShatDown Finish.")
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