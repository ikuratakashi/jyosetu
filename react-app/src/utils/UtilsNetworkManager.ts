/**
 * @ikuratakashi
 * ネットワーク関係をまとめたクラス
 */

import {UtilsLogger} from './UtilsLogger'

/**
 * WebSocketへの接続パネルのパラメタのインターフェース
 */
export interface CtrlWebSocketProps{
    ServerIp : string;
    PortNo : number;
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
        PortNo : 8080
    }

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
     * WebSocketのサーバの設定を行う
     * @param pServerParam - WebSocketのパラメタ（サーバIPなど）
     */
    InitSocketServer(pServerParam:CtrlWebSocketProps){
        this.ServerData = pServerParam;
        this.WsUri = `ws:${this.ServerData.ServerIp}:${this.ServerData.PortNo}`
    }

    /**
     * WebSocketサーバへの接続
     */
    ConnectWs(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.DoWsOpenConnecting();
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
        this.DoWsCloseConnect();
    }

    /**
     * WebSocketサーバの接続がクローズした時
     */
    onWsColeConnection(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.DoWsCloseConnect();
    }

    /**
     * WebSocketサーバーで接続が完了した時
     */
    onWsOpenConnection(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.DoWsOpenConnect();
    }

    /**
     * WebSocketサーバの接続解除時に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    DoWsCloseConnect(){}

    /**
     * WebSocketサーバの接続を開始した時に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    DoWsOpenConnecting(){}

    /**
     * WebSocketサーバの接続が完了に呼ぶメソッド
     * ※このメソッドに各処理で動きを割り当てる
     */
    DoWsOpenConnect(){}

    /**
     * WebSocketサーバーにメッセージを送る
     * @param pMessage - エラーメッセージ
     */
    sendWsMessage(pMessage:string){

        if (this.Socket && this.Socket.readyState === WebSocket.OPEN) {
            this.Socket.send(pMessage);
            this.Logger.Log(`${this.Logger.getMethodName()}():${pMessage}`);
          } else {
            this.Logger.LogError(`${this.Logger.getMethodName()}():WebSocket is not open or is null.`);
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