import { useState, useEffect, useRef } from 'react';
import DashboardContent from './dashboard/Dashboard';
import * as UtilsNetworkManager from './utils/UtilsNetworkManager';

const App = () => {//

  //.envファイルの読み込み
  const ws_env :UtilsNetworkManager.EnvNetworkManager = {
    ws_mode : process.env.REACT_APP_WEBSOCKET_MODE,
    ws_host : process.env.REACT_APP_WEBSOCKET_HOST,
    ws_port : process.env.REACT_APP_WEBSOCKET_PORT,
    ws_protcol : process.env.REACT_APP_WEBSOCKET_PROTOCOL,
  }
  
  //通信関係のモジュール
  const NetWorkManager = new UtilsNetworkManager.NetworkManager(ws_env);

  //ダッシュボードの画面表示
  const props ={
    networkmanager:NetWorkManager
  };
  return <DashboardContent {...props} />;

};

export default App;