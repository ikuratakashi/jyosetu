/**
 * @ikuratakashi
 * ネットワーク関係をまとめたクラス
 */

import {UtilsLogger} from './UtilsLogger'

/**
 * WebSocketへの接続パネルのパラメタのインターフェース
 */
export interface CtrlWebSocketProps{
    ServerIp : string | undefined;
    PortNo : string | undefined;
    Protocol : string | undefined;
}

/**
 * 設定値
 */
export interface EnvNetworkManager{
    ws_mode : string | undefined,
    ws_host : string | undefined,
    ws_port : string | undefined,
    ws_protcol : string | undefined,
}

/**
 * ネットワーク関係のマネージャー
 */
export class NetworkManager {

    /**
     * サーバー情報
     */
    ServerData : CtrlWebSocketProps = {
        /*
         * WebSocketサーバのIP
         */
        ServerIp :"127.0.0.1",
        /**
         * WebSocketのポート番号
         */
        PortNo : "8080",
        /**
         * WebSocketのプロトコル
         */
        Protocol : "ws"
    }

    /**
     * 設定
     */
    Env : EnvNetworkManager = {} as EnvNetworkManager;

    /**
     * WebSocketアドレス
     */
    WsUri : string = "";

    /**
     * WebSocketオブジェクト
     */
    Socket : WebSocket | null = null;

    /**
     * logger
     */
    Logger : UtilsLogger = new UtilsLogger();

    /**
     * コンストラクタ 
     */
    constructor(pEnv:EnvNetworkManager){
        //設定
        this.Env = pEnv;
        if(this.Env.ws_mode == "auto"){
            this.AutoInit();
        }
        //WebSocketサーバを初期値で設定
        this.InitSocketServer(this.ServerData);
    }

    /**
     * 初期設定の自動設定
     */
    AutoInit(){
        // eslint-disable-next-line no-restricted-globals
        const isSSL = location.protocol === 'https:';
        const wsProtocol = isSSL ? 'wss' : 'ws';
        this.ServerData.Protocol = wsProtocol + ":";
        // eslint-disable-next-line no-restricted-globals
        const beforeColon = location.host.split(':')[0];
        this.ServerData.ServerIp = beforeColon;
        this.ServerData.PortNo = this.Env.ws_port;
        //this.InitSocketServer(this.ServerData);
        //this.onWsAutoInitAfterEx();
    }

    /**
     * WebSocketのサーバの設定を行う
     * @param pServerParam - WebSocketのパラメタ（サーバIPなど）
     */
    InitSocketServer(pServerParam:CtrlWebSocketProps){
        this.ServerData = pServerParam;
        this.WsUri = `${this.ServerData.Protocol}//${this.ServerData.ServerIp}:${this.ServerData.PortNo}`
    }

    /**
     * 引数の値からサーバ情報をパースする
     * @param pUrl - パースする値
     */
    SocketServerDataParsSet(pUrl:string){
        try{
            const urlParts = new URL(pUrl);
            this.ServerData.Protocol = urlParts.protocol;
            this.ServerData.ServerIp = urlParts.hostname;
            this.ServerData.PortNo = urlParts.port;
            this.InitSocketServer(this.ServerData);
        }catch{

        }
    }

    /**
     * WebSocketサーバへの接続
     */
    ConnectWs(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.onWsOpenConnectingEx();
        this.Socket = new WebSocket(this.WsUri);
        this.Socket.onopen = this.onWsOpenConnection.bind(this);
        this.Socket.onmessage = this.onWsMessage.bind(this);
        this.Socket.onerror = this.onWsError.bind(this);
        this.Socket.onclose = this.onWsColeConnection.bind(this);
    }

    /**
     * WebSocketサーバの接続解除
     */
    CloseWsConnect(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        if(this.Socket){
            this.Socket.close();
            this.Socket = null;
        }
        this.onWsCloseConnectEx();
    }

    /**
     * WebSocketサーバの接続がクローズした時
     */
    onWsColeConnection(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.onWsCloseConnectEx();
    }

    /**
     * WebSocketサーバーで接続が完了した時
     */
    onWsOpenConnection(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.onWsOpenConnectEx();
    }

    /**
     * WebSocketサーバの接続解除時に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    onWsCloseConnectEx(){}

    /**
     * WebSocketサーバの接続を開始した時に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    onWsOpenConnectingEx(){}

    /**
     * WebSocketサーバの接続が完了に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    onWsOpenConnectEx(){}

    /**
     * WebSocketの自動設定が完了したときに呼ぶメソッド
     */
    onWsAutoInitAfterEx(){}

    /**
     * WebSocketサーバーにメッセージを送る
     * @param pMessage - エラーメッセージ
     */
    sendWsMessage(pMessage:string){

        if (this.Socket && this.Socket.readyState === WebSocket.OPEN) {
            this.Socket.send(pMessage);
            this.Logger.Log(`${this.Logger.getMethodName()}():${pMessage}`);
          } else {
            this.Logger.LogError(`${this.Logger.getMethodName()}(${pMessage}):WebSocket is not open or is null.`);
          }
      
    }

    /**
     * WebScoketサーバからのメッセージの受信時
     * @param event - WebSocketサーバからの値
     */
    onWsMessage(event:any){
        this.Logger.Log(`${this.Logger.getMethodName()}("${event}")`);
    }

    /**
     * WebSocketのエラー発生時
     * @param error - エラー内容
     */
    onWsError(error:any){
        this.Logger.LogError('WebSocket error: ', error);
    }

    /**
     * クラスのインスタンスを開放するときに呼ぶメソッド
     */
    public destory(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.CloseWsConnect();
    }

}