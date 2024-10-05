import socket

class CommonUtil:
    '''
    共通モジュール
    '''
    def GetLocalIp():
        '''
        ローカルIPアドレスの取得
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # 接続を試みる（実際には接続しない）
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
