/**
 * @ikuratakashi
 * ネットワーク関係をまとめたクラス
 */

import {UtilsLogger} from './UtilsLogger'
import {DateNow} from './UtilsCommon';
import {MomoServerProps} from './UtilsCommon';

/**
 * <select>の中身用
 */
export interface MomoServerSelectList extends MomoServerProps{
    /**
     * \<select\>のvalue
     */
    value? : string ,
    /**
     * \<select\>のlabel
     */
    label? : string 
}

/**
 * momoのサーバの設定
 */
export class MomoServer{

    /**
     * サーバーの設定(初期値)
     */
    ServerData : MomoServerSelectList = {
        /*
         * WebSocketサーバのIP
         */
        ServerIp : "127.0.0.1",
        /**
         * WebSocketのポート番号
         */
        PortNo : "8080",
        /**
         * WebSocketのプロトコル
         */
        Protocol : "ws",

        /**
         * デバイス名
         */
        DeviceName : "Server1",

        /**
         * 映像のコーデック
         */
        Codec : 'H264',

        /**
         * サーバの使用
         */
        Used : false,

    }

    /**
     * コンストラクタ
     * @param pProps - 設定するサーバー設定
     */
    constructor(pProps : MomoServerProps){

        Object.assign(this.ServerData, pProps);

        //<select>ようの情報を作成
        this.ServerData.label = `${this.ServerData.Protocol}://${this.ServerData.ServerIp}:${this.ServerData.PortNo}`;
        this.ServerData.value = this.ServerData.DeviceName;

        //console.log(`MomoServer prop: ${JSON.stringify(this.ServerData, null, 2)}`);

    }
}

/**
 * momoのサーバを管理する
 */
export class MomoManager{

    /**
     * サーバーリスト
     */
    ServerItems : MomoServer[] = [];

    /**
     * Momoの動画配信
     */
    VideoItems : MomoVideo[] = [];

    /**
     * MomoのVideoItemsのカウント
     */
    VideoCounter : number = 0;

    /**
     * コーデック
     */
    CodecItems :{value:string,label:string} [] = [
        { value: 'H264', label: 'H264'},
        { value: 'VP8' , label: 'H264'},
        { value: 'VP9' , label: 'VP8' },
        { value: 'AV1' , label: 'AV1' }
    ];

    /**
     * MomoServerを追加する
     * @param pProps - MomoServerの設定
     * @returns - 追加したMomoServer
     */
    addMomoServer(pProps : MomoServerProps) : MomoServer{
        this.ServerItems.push(new MomoServer(pProps));
        return this.ServerItems[this.ServerItems.length - 1];
    }

    /**
     * サーバ情報を\<select\>の内容で返す
     * @returns \<select\>の内容
     */
    cleateServerSelectList() : any[] {

        let result : any = [];

        this.ServerItems.forEach((serverItem: MomoServer, index) => {
            if(serverItem.ServerData){
                result.push
                (
                    {
                        label : `${serverItem.ServerData.label}`,
                        value : serverItem.ServerData.value
                    }
                );
            }
        });

        return result;

    }

    /**
     * 使用するMomoServerの選択設定
     * @param pDeviceName - 選択したDeviceName
     * @param pUsed - 選択状態 (True/False)
     */
    /*
    setUsedMomoserver(pDeviceName:string,pUsed:boolean){
        for (let server of this.ServerItems) {
            if (server.ServerData.DeviceName === pDeviceName) {
                server.ServerData.Used = pUsed;
                break;
            }
        }
    }
    */


    /**
     * 映像情報を追加する
     * @param props 映像を再生するエレメントやサーバ情報など
     * @returns momoの映像情報
     */
    addVideoItem(props : MomoVideoProps) : MomoVideo{
        this.VideoCounter++;
        props.Name = `${this.VideoCounter}-${DateNow()}`;
        this.VideoItems.push
        (
            new MomoVideo(props)
        );
        return this.VideoItems[this.VideoItems.length - 1];
    }

    /**
     * 映像情報を削除する
     * @param pMomoVideo - 削除するMomoVideo
     */
    removeVideItem(pMomoVideo:MomoVideo){
        this.VideoItems = this.VideoItems.filter(item => item.props?.Name !== pMomoVideo.props?.Name);
    }

}


/**
 * Class MomoVideoのパラメタ
 */
export interface MomoVideoProps{

    /**
     * 識別するための名前
     */
    Name? : string | undefined;

    /**
     * momoのサーバ情報
     */
    MomoServerData : MomoServer | undefined;

    /**
     * ビデオのエレメント
     */
    VideoElement : HTMLVideoElement | null;

    /**
     * コーデック
     */
    Codecs : string | undefined;
}

/**
 * iceServersのインターフェース
 */
interface interface_iceServers {
    /**
     * Url
     */
    urls : string
}

/**
 * Momoの動画を受信して表示するクラス
 */
export class MomoVideo{

    /**
     * 引数
     */
    props : MomoVideoProps | undefined;

    peerConnection : RTCPeerConnection | undefined;
    dataChannel : RTCDataChannel | undefined;
    candidates : RTCIceCandidate[] | undefined;
    hasReceivedSdp :boolean = false;

    /**
     * iceServer を定義
     */ 
    iceServers : interface_iceServers[] | undefined = 
    [
        {'urls': 'stun:stun.l.google.com:19302'}
    ];

    /**
     * peer connection の 設定
     */
    peerConnectionConfig : {iceServers : interface_iceServers[] | undefined} = {
      'iceServers': this.iceServers
    };

    /**
     * WebSocket
     */
    ws : WebSocket | undefined = undefined;

    /**
     * Logger
     */
    Logger : UtilsLogger = new UtilsLogger();

    /**
     * VideoのElement
     */
    remoteVideo : HTMLVideoElement | null;

    /**
     * コンストラクタ
     * @param prop プロパティ
     */
    constructor(pProps : MomoVideoProps){

        this.Logger.ConsoleGroupSet();
        this.Logger.Log(`MomoVideo.constructor()`);

        /**
         * プロパティ
         */
        this.props = pProps;

        this.remoteVideo = this.props.VideoElement;

        this.Logger.consoleGroupEnd();

    }

    /**
     * WebSocketを設定する
     */
    SetWebSocket(){

        /**
         * WebSocket
         */
        const ServerData = this.props?.MomoServerData?.ServerData;
        const Url = `${ServerData?.Protocol}://${ServerData?.ServerIp}:${ServerData?.PortNo}/ws`;

        this.Logger.Log(`new Websocket('${Url}')`);

        this.ws = new WebSocket(Url);

        this.ws.onerror = this.WsError.bind(this);
        this.ws.onopen = this.WsOpen.bind(this);
        this.ws.onmessage = this.WsMessage.bind(this);

    }

    /**
     * WebSocketの接続がオープンしたときの処理
     * @param pEvent Event
     */
    WsOpen(event:Event){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.WsOpenEx();
    } 

    /**
     * WebSocketのエラー処理
     * @param error - Error
     */
    WsError(error : Event){
        this.Logger.LogError(`${this.Logger.getMethodName()}():`,error)
        this.WsErrorEx();
    }

    /**
     * WebSocketのエラー時に実行される処理を設定する
     */
    WsErrorEx(){};

    /**
     * WebSocketでメッセージを受信したときの処理
     * @param event Event
     */
    WsMessage(event:any){

        this.Logger.Log(`${this.Logger.getMethodName()}():data:`,event.data);

        const message = JSON.parse(event.data);
        if (message.type === 'offer') {
            const offer = new RTCSessionDescription(message);
            this.Logger.Log(`${this.Logger.getMethodName()}():Received offer`,offer);
            this.setOffer(offer);
        }
        else if (message.type === 'answer') {
          const answer = new RTCSessionDescription(message);
          this.Logger.Log(`${this.Logger.getMethodName()}():Received answer:`,answer);
          this.setAnswer(answer);
        }
        else if (message.type === 'candidate') {
          console.log('Received ICE candidate ...');
          const candidate = new RTCIceCandidate(message.ice);
          console.log('candidate: ', candidate);

          this.Logger.Log(`${this.Logger.getMethodName()}():Received ICE candidate:`,candidate);

          if (this.hasReceivedSdp) {
            this.addIceCandidate(candidate);
          } else {
            if(!this.candidates){
                this.candidates = [];
            }
            this.candidates.push(candidate);
          }
        }
        else if (message.type === 'close') {
            this.Logger.Log(`${this.Logger.getMethodName()}():peer connection is closed ...`);
        }

        /**
         * WebSocketでメッセージを受け取った時処理を実行
         */
        this.WsMessageEx();
    }

    /**
     * WebSocketでメッセージを受信した時に実行される処理
     */
    WsMessageEx(){};

    /**
     * WebSocketの接続のオープン時に実行される処理を設定する
     */
    WsOpenEx(){};

    /**
     * 接続
     */
    connect(){

        this.Logger.Log(`${this.Logger.getMethodName()}()`);

        this.Logger.ConsoleGroupSet();
        this.Logger.Log(`[${this.props?.Name}] connect:${JSON.stringify(this.props?.MomoServerData?.ServerData, null, 2)}`);

        if (!this.peerConnection) {
            this.Logger.Log(`make Offer`);
            this.makeOffer();
        }
        else 
        {
            this.Logger.Log(`peer connection already exists.`);
        }

        this.Logger.consoleGroupEnd();
    }

    /**
     * 切断
     */
    disconnect(){
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();
        this.Logger.Log(`[${this.props?.Name}] disconnect:${JSON.stringify(this.props?.MomoServerData?.ServerData, null, 2)}`);

        if (this.peerConnection) {
            if (this.peerConnection.iceConnectionState !== 'closed') {
              this.peerConnection.close();
              this.peerConnection = undefined;
              if (this.ws && this.ws.readyState === 1) {
                const message = JSON.stringify({ type: 'close' });
                this.ws.send(message);
              }
              this.Logger.Log('sending close message');
              this.cleanupVideoElement(this.remoteVideo);
              return;
            }
        }
        this.Logger.Log('peerConnection is closed.');
        
        this.Logger.consoleGroupEnd();
    }

    /**
     * 何の処理かわからない
     */
    drainCandidate() {
        this.hasReceivedSdp = true;
        this.candidates?.forEach((candidate) => {
          this.addIceCandidate(candidate);
        });
        this.candidates = [];
    }
      
    /**
     * 何の処理かわからない
     */
    addIceCandidate(candidate:any) {
        if (this.peerConnection) {
          this.peerConnection.addIceCandidate(candidate);
        }
        else {
            this.Logger.LogError(`${this.Logger.getMethodName()}():PeerConnection does not exist!`);
        }
    }

    /**
     * 何の処理かわからない
     */
    sendIceCandidate(candidate : any) {
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();
        const message = JSON.stringify({ type: 'candidate', ice: candidate });
        this.Logger.Log(`sending candidate message:${message}`);
        this.Logger.consoleGroupEnd();
        this.ws?.send(message);
    }

    /**
     * ビデオのエレメントにストリームを設定する
     * @param element ビデオのエレメント
     * @param stream 動画ストリーム
     */
    playVideo(element : any, stream : any) {
        element.srcObject = stream;
    }

    /**
     * RTCPeerConnectionを作成する
     * @returns - RTCPeerConnection
     */
    prepareNewConnection() : RTCPeerConnection {
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();
        const peer = new RTCPeerConnection(this.peerConnectionConfig);
        this.dataChannel = peer.createDataChannel("serial");
        if ('ontrack' in peer) {
            if (this.isSafari()) {
                let tracks:MediaStreamTrack[] = [];
                peer.ontrack = (event) => {
                    this.Logger.ConsoleGroupSet();
                    this.Logger.Log('-- peer.ontrack()');
                    tracks.push(event.track)
                    // safari で動作させるために、ontrack が発火するたびに MediaStream を作成する
                    let mediaStream = new MediaStream(tracks);
                    this.playVideo(this.remoteVideo, mediaStream);
                    this.Logger.consoleGroupEnd();
                };
            }else{
                let mediaStream = new MediaStream();
                this.playVideo(this.remoteVideo, mediaStream);
                this.remoteVideo?.play();
                peer.ontrack = (event) => {
                    this.Logger.ConsoleGroupSet();
                    this.Logger.Log('-- peer.ontrack()');
                    mediaStream.addTrack(event.track);
                    this.Logger.consoleGroupEnd();
                };
            }
        /*
        } else {
            peer.onaddstream = (event : any) => {
                this.Logger.Log('-- peer.onaddstream()');
                this.playVideo(this.remoteVideo, event.stream);
            };
        */
        }

        peer.onicecandidate = (event) => {
            this.Logger.Log('-- peer.onicecandidate()');
            this.Logger.ConsoleGroupSet();
            if (event.candidate) {
                this.Logger.Log("event.candidate:",event.candidate);
                this.sendIceCandidate(event.candidate);
            } else {
                this.Logger.Log('empty ice event');
            }
            this.Logger.consoleGroupEnd();
        };

        peer.oniceconnectionstatechange = () => {
            this.Logger.Log('-- peer.oniceconnectionstatechange()');
            this.Logger.ConsoleGroupSet();
            this.Logger.Log('ICE connection Status has changed to ' + peer.iceConnectionState);
            switch (peer.iceConnectionState) {
                case 'closed':
                case 'failed':
                case 'disconnected':

                    /********************************************** */
                    /* 接続エラー時の処理 */
                    /********************************************** */

                    this.WsErrorEx();

                    /********************************************** */
                    break;
            }
            this.Logger.consoleGroupEnd();
        };

        peer.addTransceiver('video', {direction: 'recvonly'});
        peer.addTransceiver('audio', {direction: 'recvonly'});

        this.dataChannel.onmessage =  (event : any) => {
            this.Logger.ConsoleGroupSet();
            this.Logger.Log("Got Data Channel Message:", new TextDecoder().decode(event.data));
            this.Logger.consoleGroupEnd();
        };

        this.Logger.consoleGroupEnd();

        return peer;
    }
    
    /**
     * ブラウザの種類を返す
     * @returns ブラウザ種類
     */
    browser() : string {
        const ua = window.navigator.userAgent.toLocaleLowerCase();
        if (ua.indexOf('edge') !== -1) {
          return 'edge';
        }
        else if (ua.indexOf('chrome')  !== -1 && ua.indexOf('edge') === -1) {
          return 'chrome';
        }
        else if (ua.indexOf('safari')  !== -1 && ua.indexOf('chrome') === -1) {
          return 'safari';
        }
        else if (ua.indexOf('opera')   !== -1) {
          return 'opera';
        }
        else if (ua.indexOf('firefox') !== -1) {
          return 'firefox';
        }
        return "";
    }
    
    /**
     * ブラウザがsafariかどうかを返す
     * @returns True:Safari
     */
    isSafari() :boolean {
        return this.browser() === 'safari';
    }

    /**
     * sendSdp
     * @param sessionDescription 送信するメッセージ
     */
    sendSdp(sessionDescription : any) {
        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();

        const message = JSON.stringify(sessionDescription);
        this.Logger.Log('sending SDP' , message);

        this.ws?.send(message);

        this.Logger.consoleGroupEnd();
    }

    /**
     * offerの作成
     */
    async makeOffer() {

        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();

        this.peerConnection = this.prepareNewConnection();
        try {

            const sessionDescription = await this.peerConnection.createOffer({
                'offerToReceiveAudio': true,
                'offerToReceiveVideo': true
            });

            this.Logger.Log('createOffer() success in promise, SDP=', sessionDescription.sdp);

            switch (this.props?.Codecs) {
                case 'H264':
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP8');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP9');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'AV1');
                    break;
                case 'VP8':
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'H264');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP9');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'AV1');
                    break;
                case 'VP9':
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'H264');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP8');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'AV1');
                    break;
                case 'AV1':
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'H264');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP8');
                    sessionDescription.sdp = this.removeCodec(sessionDescription.sdp, 'VP9');
                    break;
            }

            await this.peerConnection.setLocalDescription(sessionDescription);
            this.Logger.Log('setLocalDescription() success in promise');

            this.sendSdp(this.peerConnection.localDescription);

        } catch (error) {
            this.Logger.LogError('makeOffer() ERROR:', error);
        }
        this.Logger.consoleGroupEnd();
    }

    /**
     * Answerを作成する
     */
    async makeAnswer() {

        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();

        this.Logger.Log('sending Answer. Creating remote session description...');

        if (!this.peerConnection) {
            this.Logger.LogError('peerConnection DOES NOT exist!');
        }else{
            try {
                const sessionDescription = await this.peerConnection.createAnswer();
                this.Logger.Log('createAnswer() success in promise');
                await this.peerConnection.setLocalDescription(sessionDescription);
                this.Logger.Log('setLocalDescription() success in promise');
                this.sendSdp(this.peerConnection.localDescription);
                this.drainCandidate();
            } catch (error) {
                this.Logger.LogError('makeAnswer() ERROR:', error);
            }
        }

        this.Logger.consoleGroupEnd();

    }

    /**
     * offer sdp を生成する
     * @param sessionDescription 
     */
    setOffer(sessionDescription : RTCSessionDescription) {

        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();

        if (this.peerConnection) {
            this.Logger.LogError('peerConnection already exists!');
        }
        const peerConnection = this.prepareNewConnection();
        peerConnection.onnegotiationneeded = async () => {
            try{
                await peerConnection.setRemoteDescription(sessionDescription);
                this.Logger.Log('setRemoteDescription(offer) success in promise');
                this.makeAnswer();
            }catch(error) {
                this.Logger.LogError('setRemoteDescription(offer) ERROR: ', error);
            }
        }

        this.Logger.consoleGroupEnd();

    }
  
    /**
     * Anserをセットする
     * @param sessionDescription 
     */
    async setAnswer(sessionDescription : RTCSessionDescription) {

        this.Logger.Log(`${this.Logger.getMethodName()}()`);
        this.Logger.ConsoleGroupSet();

        if (!this.peerConnection) {
            this.Logger.LogError('peerConnection DOES NOT exist!');
        }else{
            try {
                await this.peerConnection.setRemoteDescription(sessionDescription);
                this.Logger.Log('setRemoteDescription(answer) success in promise');
                this.drainCandidate();
            } catch(error) {
                this.Logger.LogError('setRemoteDescription(answer) ERROR: ', error);
            }
        }

        this.Logger.consoleGroupEnd();

    }

    /**
     * ビデオを停止してクリアする
     * @param element ビデオのElemet
     */
    cleanupVideoElement(element:any) {
        element.pause();
        element.srcObject = null;
    }

    /**
     * 
     * @param orgsdp 
     * @param codec 
     * @returns 
     * Stack Overflow より引用: https://stackoverflow.com/a/52760103
     * https://stackoverflow.com/questions/52738290/how-to-remove-video-codecs-in-webrtc-sdp
     */
    removeCodec(orgsdp : any, codec : any) : any | undefined {

        const internalFunc = (sdp:any):any => {

            const codecre = new RegExp('(a=rtpmap:(\\d*) ' + codec + '\/90000\\r\\n)');
            const rtpmaps = sdp.match(codecre);
            if (rtpmaps == null || rtpmaps.length <= 2) {
                return sdp;
            }
            const rtpmap = rtpmaps[2];
            let modsdp = sdp.replace(codecre, "");
        
            const rtcpre = new RegExp('(a=rtcp-fb:' + rtpmap + '.*\r\n)', 'g');
            modsdp = modsdp.replace(rtcpre, "");
        
            const fmtpre = new RegExp('(a=fmtp:' + rtpmap + '.*\r\n)', 'g');
            modsdp = modsdp.replace(fmtpre, "");
        
            const aptpre = new RegExp('(a=fmtp:(\\d*) apt=' + rtpmap + '\\r\\n)');
            const aptmaps = modsdp.match(aptpre);
            let fmtpmap = "";
            if (aptmaps != null && aptmaps.length >= 3) {
                fmtpmap = aptmaps[2];
                modsdp = modsdp.replace(aptpre, "");
            
                const rtppre = new RegExp('(a=rtpmap:' + fmtpmap + '.*\r\n)', 'g');
                modsdp = modsdp.replace(rtppre, "");
            }
        
            let videore = /(m=video.*\r\n)/;
            const videolines = modsdp.match(videore);
            if (videolines != null) {
                //If many m=video are found in SDP, this program doesn't work.
                let videoline = videolines[0].substring(0, videolines[0].length - 2);
                const videoelems = videoline.split(" ");
                let modvideoline = videoelems[0];
                videoelems.forEach((videoelem:any, index:any) => {
                    if (index === 0) return undefined;
                    if (videoelem == rtpmap || videoelem == fmtpmap) {
                        return undefined;
                    }
                    modvideoline += " " + videoelem;
                })
                modvideoline += "\r\n";
                modsdp = modsdp.replace(videore, modvideoline);
            }
            return internalFunc(modsdp);
        }

        return internalFunc(orgsdp);
    }

    /**
     * ビデオの再生
     */
    play() {
        this.remoteVideo?.play();
    }

}