import sys
import serial
from env import clsEnvData 
from Log import clsLog
import inspect
import signal
from colorama import init, Fore, Back, Style
import time
import usbdev

UsbDevice : usbdev.clsUsbDevice  = None
CmmandSendSerial : serial.Serial = None
IsShutdown = False

def SerialOpen(pDev:str = "") -> bool:
    '''
    シリアル通信を開く
    戻り値：オープンの成功:True／失敗:False
    '''
    cur = inspect.currentframe().f_code.co_name
    IsError = False
    Result = True
    EnvData : clsEnvData = clsEnvData()
    Log = clsLog()

    global CmmandSendSerial
    global UsbDevice

    UsbDevice = usbdev.clsUsbDevice()
    UsbDevice.SearchUsbList()
    SelDev = ""

    if pDev == "" and len(UsbDevice.UsbSirialList) > 0:
        SelDev = UsbDevice.UsbSirialList[len(UsbDevice.UsbSirialList)-1].Name
    else:
        SelDev = pDev

    try:
        CmmandSendSerial = serial.Serial(SelDev, EnvData.RS232C_BPS, timeout=EnvData.RS232C_TIMEOUT,xonxoff=True)
        Log.LogOut(cur,clsLog.TYPE_RS232C,f"Serial Open Device:{Back.GREEN} {EnvData.RS232C_DEV_RECV} {Back.RESET}")
    except serial.SerialException as e:
        Log.LogOut(cur,clsLog.TYPE_ERR,f"Serial error:{e}")
        IsError = True
    except Exception as e:
        Log.LogOut(cur,clsLog.TYPE_ERR,f"Unexpected error:{e}")
        IsError = True

    if IsError == True:
        Result = False
        if pDev == "" :
            if len(UsbDevice.UsbSirialList) > 0:
                for Device in UsbDevice.UsbSirialList[::-1]:
                    IsOpen = SerialOpen(Device.Name)
                    if IsOpen == True:
                        Result = True
                        Log.LogOut(cur,clsLog.TYPE_ERR,f"CommandSend Serial No Open Device:{Back.YELLOW} {EnvData.RS232C_DEV_RECV} {Back.RESET}")
                        Log.LogOut(cur,clsLog.TYPE_WAR,f"CommandSend Serial Re Open Device:{Back.WHITE} {Device} {Back.RESET}")
                        break
    
    return Result

def main():

    cur = inspect.currentframe().f_code.co_name
    log : clsLog = clsLog()

    global CmmandSendSerial
    EnvData : clsEnvData = clsEnvData()

    print("--------------------------")
    print("START RS232C Recv")
    print("--------------------------")
    print("ShutDown : Ctrl + C")
    print("--------------------------")

    SerialOpen()

    while True:
        if IsShutdown == True :
            break
        try:
            #if CmmandSendSerial.in_waiting > 0:
            if True:
                data_raw=CmmandSendSerial.readline().decode('utf-8',errors="ignore").rstrip()
                data_list=data_raw.split(",")
                data_show=[]
                for data in data_list:

                    if data == "c_up" or data == "c_dw":
                        data = f"{Style.RESET_ALL}{data}"
                    else:
                        data = f"{Fore.YELLOW}{data}{Style.RESET_ALL}"

                    data_show.append(data)

                log.LogOut(cur,clsLog.TYPE_RS232C,f"Received:{','.join(data_show)}")
        except Exception as e:
            log.LogOut(cur,clsLog.TYPE_WAR,f"Serial Closed Device:{EnvData.RS232C_DEV_RECV}")
            log.LogOut(cur,clsLog.TYPE_ERR,f"{e}")
            SerialOpen()
            time.sleep(2)

def shutdown():

    global CmmandSendSerial
    global IsShutdown

    if CmmandSendSerial != None and CmmandSendSerial.is_open == True:
        CmmandSendSerial.close()

    IsShutdown = True
    print("Shutdown")
    sys.exit(0)

if __name__ == "__main__":

    #プログラム終了時のハンドリング
    signal.signal(signal.SIGINT,lambda sig, frame: shutdown())

    main()