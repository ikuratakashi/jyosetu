import sqlite3
from env import clsEnvData 
from Log import clsLog
from Error import clsError
import inspect
from datetime import datetime,timedelta
from colorama import Back, Style

class clsDB(clsLog,clsError):
    '''
    DBクラス
    '''

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
        コマンドをテーブルに追加する
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
