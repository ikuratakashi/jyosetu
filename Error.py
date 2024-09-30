from Log import clsLog

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
