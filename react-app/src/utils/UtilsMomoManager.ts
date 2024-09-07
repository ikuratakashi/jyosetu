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
    VideoElement : React.MutableRefObject<null> | undefined;

    /**
     * コーデック
     */
    Codecs : string | undefined;
}

/**
 * Momoの動画を受信して表示するクラス
 */
export class MomoVideo{

    /**
     * 引数
     */
    props : MomoVideoProps | undefined;

    /**
     * コンストラクタ
     * @param prop プロパティ
     */
    constructor(pProps : MomoVideoProps){
        this.props = pProps;
    }

    /**
     * 接続
     */
    connect(){
        console.log(`[${this.props?.Name}] connect:${JSON.stringify(this.props?.MomoServerData?.ServerData, null, 2)}`);
    }

    /**
     * 切断
     */
    disconnect(){
        console.log(`[${this.props?.Name}] disconnect:${JSON.stringify(this.props?.MomoServerData?.ServerData, null, 2)}`);
    }

}