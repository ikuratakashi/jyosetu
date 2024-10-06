class clsCameraData():
    '''
    カメラデータ
    '''
    DeviceName : str = ""
    '''
    デバイス名
    '''
    Codec : str = "H264"
    '''
    コーデック
    '''
    PortNo : str = ""
    '''
    ポート番号
    '''
    Protocl : str = "ws"
    '''
    プロトコル
    '''
    ServerIp : str = ""
    '''
    IPアドレス
    '''
    ProcessId : int = 0
    '''
    プロセス番号
    '''

    def __init__(self,
                 DeviceName:str,
                 PortNo:str,
                 Protocl : str = "ws",
                 ServerIp:str = "127.0.0.1",
                 Codec:str = "H264",
                 ProcessId:int = 0
                 ):
        '''
        コンストラクタ
        '''
        self.DeviceName = DeviceName
        self.Codec = Codec
        self.PortNo = PortNo
        self.Protocl = Protocl
        self.ServerIp = ServerIp
        self.ProcessId = ProcessId

