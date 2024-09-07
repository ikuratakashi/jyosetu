import { useState, useEffect, useRef } from 'react';
import DashboardContent from './dashboard/Dashboard';
import {EnvNetworkManager,MomoServerProps} from './utils/UtilsCommon';
import * as UtilsNetworkManager from './utils/UtilsNetworkManager';
import * as UtilsMomoManager from './utils/UtilsMomoManager';


const App = () => {//

  //.envファイルの読み込み
  const ws_env :EnvNetworkManager = {
    ws_mode : process.env.REACT_APP_WEBSOCKET_MODE,
    ws_host : process.env.REACT_APP_WEBSOCKET_HOST,
    ws_port : process.env.REACT_APP_WEBSOCKET_PORT,
    ws_protcol : process.env.REACT_APP_WEBSOCKET_PROTOCOL,
  }
  
  //通信関係のモジュール
  const NetWorkManager = new UtilsNetworkManager.NetworkManager(ws_env);

  //カメラ関係のモジュール
  const MomoManager = new UtilsMomoManager.MomoManager();
  if(true){
    MomoManager.addMomoServer({
      DeviceName : "server1",
      Codec : "H264",
      PortNo : "51001",
      Protocol : "ws",
      ServerIp : "192.168.1.1",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server2",
      Codec : "H264",
      PortNo : "51002",
      Protocol : "ws",
      ServerIp : "192.168.1.1",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server3",
      Codec : "H264",
      PortNo : "51003",
      Protocol : "ws",
      ServerIp : "192.168.1.1",
      Used : false,
    })
  }

  //ダッシュボードの画面表示
  const props ={
    networkmanager:NetWorkManager,
    momomanager:MomoManager
  };
  return <DashboardContent {...props} />;

};

export default App;