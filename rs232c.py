import sys
import serial
from env import clsEnvData 
from Log import clsLog
import inspect
import signal

ser : serial.Serial = None
IsShutdown = False

def main():

    print("--------------------------")
    print("START RS232C Recv")
    print("--------------------------")
    print("ShutDown : Ctrl + C")
    print("--------------------------")

    cur = inspect.currentframe().f_code.co_name
    e = clsEnvData()
    log : clsLog = clsLog()

    ser = serial.Serial(port=e.RS232C_DEV_RECV,baudrate=e.RS232C_BPS,timeout=e.RS232C_TIMEOUT)

    while True:
        if IsShutdown == True :
            break
        try:
            if ser.in_waiting > 0:
                data=ser.readline().decode('utf-8',errors="ignore").rstrip()
                log.LogOut(cur,clsLog.TYPE_LOG,f"Received:{data}")
        except Exception as e:
            log.LogOut(cur,clsLog.TYPE_ERR,f"{e}")

def shutdown():
    if ser != None and ser.is_open == True:
        ser.close()
    IsShutdown = True
    print("Shutdown")
    sys.exit(0)

if __name__ == "__main__":

    #プログラム終了時のハンドリング
    signal.signal(signal.SIGINT,lambda sig, frame: shutdown())

    main()