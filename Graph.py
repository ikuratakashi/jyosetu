import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots, pause
import inspect
import time

from Error import clsError
from Log import clsLog
from env import clsEnvData

class clsGraph(clsLog,clsError):
    '''
    グラフを描画するクラス
    '''
    
    x_data = []
    '''
    グラフ表示用 X
    '''
    y_data = []
    '''
    グラフ表示用 Y
    '''
    fig = any
    '''
    グラフ表示用 fig
    '''
    ax = any
    '''
    グラフ表示用 ax
    '''
    IsGraphStart : bool = False
    '''
    グラフィックの開始を実行したかどうか
    '''
    GraphName : str = "sample"
    '''
    グラフ名
    '''
    Label_X : str = "X"
    '''
    X軸のラベル
    '''
    Label_Y : str = "Y"
    '''
    Y軸のラベル
    '''

    def __init__(self,IsDebug,GraphName,Label_X,Label_Y):
        '''
        コンストラクタ
        '''
        self.EnvData = clsEnvData()
        self.IsDebug = IsDebug
        self.IsGraphStart == False
        self.GraphName = GraphName
        self.Label_X = Label_X
        self.Label_Y = Label_Y
        self.x_data = []
        self.y_data = []

    def StartGraph(self):
        '''
        値をグラフで描画する処理を開始する
        '''

        if self.IsGraphStart == False:

            # グラフの設定
            plt.ion()
            self.fig,self.ax  = plt.subplots()
            self.IsGraphStart = True

    def DrawGraph(self,value):
        '''
        グラフを描画する
        '''
        #グラフ描画の開始
        self.StartGraph()

        window_size = 50

        # 表示用のデータに受信したデータを追加
        self.x_data.append(time.time())
        self.y_data.append(value)

        if len(self.x_data) > window_size:
            self.x_data = self.x_data[-window_size:]
            self.y_data = self.y_data[-window_size:]

        # グラフにデータを追加
        self.ax.clear()

        self.ax.set_title(self.GraphName, fontsize=14, fontweight='bold', color='blue')
        self.ax.set_xlabel(self.Label_X)
        self.ax.set_ylabel(self.Label_Y)
        
        self.ax.plot(self.x_data, self.y_data, color='C0', linestyle='-' , label="Data")
        self.ax.legend()
        plt.draw()
        plt.pause(0.01)

    def CloseGraph(self):
        '''
        グラフを閉じる
        '''
        cur = inspect.currentframe().f_code.co_name
        try:
            plt.close()
        except Exception as e:
            self.HandleError(cur,f"Unexpected error:{e}")
        
if __name__ == "__main__":
    # いくつかのclsGraphインスタンスを作成
    graph1 = clsGraph(IsDebug=True, GraphName="Graph 1", Label_X="Time", Label_Y="Value")
    graph2 = clsGraph(IsDebug=True, GraphName="Graph 2", Label_X="Time", Label_Y="Value")

    # グラフを更新するシミュレーション
    for i in range(100):
        graph1.DrawGraph(i)  # graph1を更新
        graph2.DrawGraph(i * 0.5)  # graph2を更新
        time.sleep(0.1)  # 0.1秒待つ

    # 最後にグラフを閉じる
    graph1.CloseGraph()
    graph2.CloseGraph()
    plt.show(block=True)