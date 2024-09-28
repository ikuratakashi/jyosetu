import DashboardContent from './dashboard/Dashboard';
import {EnvNetworkManager,EnvSendCommand,MomoServerProps} from './utils/UtilsCommon';
import * as UtilsNetworkManager from './utils/UtilsNetworkManager';
import * as UtilsMomoManager from './utils/UtilsMomoManager';


const App = () => {//

  //.envファイルの読み込み

  //ネットワーク関連
  const env_ws :EnvNetworkManager = {
    ws_mode : process.env.REACT_APP_WEBSOCKET_MODE,
    ws_host : process.env.REACT_APP_WEBSOCKET_HOST,
    ws_port : process.env.REACT_APP_WEBSOCKET_PORT,
    ws_protcol : process.env.REACT_APP_WEBSOCKET_PROTOCOL,
  }

  //ボタンを押下した時のコマンド関連
  const env_send_command :EnvSendCommand = {
    type_emergency : process.env.REACT_APP_TYPE_EMERGENCY,
    type_operation : process.env.REACT_APP_TYPE_OPERATION,
    type_sound : process.env.REACT_APP_TYPE_SOUND,
  }
  
  //通信関係のモジュール
  const NetWorkManager = new UtilsNetworkManager.NetworkManager(env_ws);

  //カメラ関係のモジュール
  const MomoManager = new UtilsMomoManager.MomoManager();
  if(true){
    MomoManager.addMomoServer({
      DeviceName : "server1",
      Codec : "H264",
      PortNo : "51001",
      Protocol : "ws",
      ServerIp : "192.168.3.14",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server2",
      Codec : "H264",
      PortNo : "51002",
      Protocol : "ws",
      ServerIp : "192.168.3.14",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server3",
      Codec : "H264",
      PortNo : "51003",
      Protocol : "ws",
      ServerIp : "192.168.3.14",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server4",
      Codec : "H264",
      PortNo : "51004",
      Protocol : "ws",
      ServerIp : "192.168.3.14",
      Used : false,
    })
    MomoManager.addMomoServer({
      DeviceName : "server5",
      Codec : "H264",
      PortNo : "51005",
      Protocol : "ws",
      ServerIp : "192.168.3.14",
      Used : false,
    })
  }

  //ダッシュボードの画面表示
  const props ={
    networkmanager:NetWorkManager,
    momomanager:MomoManager,
    envsendcommand:env_send_command,
  };
  return <DashboardContent {...props} />;

};

export default App;