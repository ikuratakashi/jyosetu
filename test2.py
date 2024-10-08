import matplotlib.pyplot as plt
import time

class GraphDrawer:
    def __init__(self):
        pass  # ここでは何も行いません

    def StartGraph(self):
        '''
        値をグラフで描画する処理を開始する
        '''
        plt.ion()  # インタラクティブなグラフを有効にする
        self.x_data = []
        self.y_data = []
        self.fig, self.ax = plt.subplots()  # 正しくフィギュアとアクシスを設定
        
        '''
        self.DrawGraph(0)
        self.DrawGraph(1)
        self.DrawGraph(2)
        self.DrawGraph(3)
        '''
    
    def DrawGraph(self, value):
        '''
        グラフを描画する
        '''
        print(value)

        self.x_data.append(time.time())
        self.y_data.append(value)
        
        # グラフにデータを追加
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, color='C0', linestyle='-', label='Sample1')
        self.ax.legend()
        plt.draw()
        plt.pause(3)

# 使用例
graph_drawer = GraphDrawer()
graph_drawer.StartGraph()
