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

    def __init__(self,
                 DeviceName:str,
                 PortNo:str,
                 Protocl : str = "ws",
                 ServerIp:str = "127.0.0.1",
                 Codec:str = "H264",
                 ):
        '''
        コンストラクタ
        '''
        self.DeviceName = DeviceName
        self.Codec = Codec
        self.PortNo = PortNo
        self.Protocl = Protocl
        self.ServerIp = ServerIp

