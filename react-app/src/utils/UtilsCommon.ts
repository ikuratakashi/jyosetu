/**
 * @ikuratakashi
 * 共通モジュール
 */
import { MomoManager } from './UtilsMomoManager';
import { NetworkManager } from './UtilsNetworkManager';
import { useRef } from 'react';

/**
 * アナログスティックの種類
 */
export enum enmAnalogSticType{
    /**
     * 左側
     */
    left = 'left',
    /**
     * 右側
     */
    right = 'right'
}

/**
 * ボタンの種類
 */
export enum enmButtonType{
    /**
    * 初期値
    */
    none        = 'none',
    /**
    * 接続/接続解除
    */
    conn        = 'conn',           
    /**
    * クラッチ アップ
    */
    clutch_up   = 'clutch_up',
    /**
    * クラッチ ダウン
    */
    clutch_dw   = 'clutch_dw', 
    /**
    * AUTOクラッチ ダウン ON
    */
    auto_clutch_dw_on   = 'auto_clutch_dw_on',
    /**
    * AUTOクラッチ ダウン OFF
    */
    auto_clutch_dw_off   = 'auto_clutch_dw_off',
    /**
    * アクセル アップ
    */
    accel_up    = 'accel_up',
    /**
    * アクセル ダウン
    */
    accel_dw    = 'accel_dw',
    /**
    * 移動 前進
    */
    move_fw     = 'move_fw',
    /**
    * 移動 後進
    */
    move_bk     = 'move_bk',
    /**
    * 移動 右
    */
    move_right  = 'move_right',
    /**
    * 移動 左
    */
    move_left   = 'move_left',

    /** -----------------------------------
     *  アナログスティックの種類：左側
    ---------------------------------------*/
    /**
    * 雪射出口 左上向き
    */
    chute_L_lup    = 'chute_L_lup',
    /**
    * 雪射出口 上向き
    */
    chute_L_up    = 'chute_L_up',
    /**
    * 雪射出口 右上向き
    */
    chute_L_rup    = 'chute_L_rup',
    /**
    * 雪射出口 右向き
    */
    chute_L_right = 'chute_L_right',
    /**
    * 雪射出口 右下向き
    */
    chute_L_rdw = 'chute_L_rdw',
    /**
    * 雪射出口 下向き
    */
    chute_L_dw    = 'chute_L_dw',
    /**
    * 雪射出口 左下向き
    */
    chute_L_ldw  = 'chute_L_ldw',
    /**
    * 雪射出口 左向き
    */
    chute_L_left  = 'chute_L_left',

    /** -----------------------------------
     *  アナログスティックの種類：右側
    ---------------------------------------*/
    /**
    * 雪射出口 スティック右 左上向き
    */
    chute_R_lup    = 'chute_R_lup',
    /**
    * 雪射出口 上向き
    */
    chute_R_up    = 'chute_R_up',
    /**
    * 雪射出口 右上向き
    */
    chute_R_rup    = 'chute_R_rup',
    /**
    * 雪射出口 右向き
    */
    chute_R_right = 'chute_R_right',
    /**
    * 雪射出口 右下向き
    */
    chute_R_rdw = 'chute_R_rdw',
    /**
    * 雪射出口 下向き
    */
    chute_R_dw    = 'chute_R_dw',
    /**
    * 雪射出口 左下向き
    */
    chute_R_ldw  = 'chute_R_ldw',
    /**
    * 雪射出口 左向き
    */
    chute_R_left  = 'chute_R_left',

    /**
     * 未設定ボタン△
     */
    btn_sankaku = 'btn_sankaku',
    /**
     * 未設定ボタン□
     */
    btn_sikaku = 'btn_sikaku',
    /**
    * 歯の回転のON
    */
    btn_on      = 'btn_on',
    /**
    * 歯の回転のOFF
    */
    btn_off     = 'btn_off',
    /**
    * 緊急停止
    */
    btn_em      = 'btn_em',
}

/**
 * 接続状態の色
 */
export enum enmConnectCorlor{
    /**
     * 未接続
     */
    disconnect = 'red',
    /**
     * 接続された
     */
    connect = 'lime',
    /**
     * 接続処理実行中
     */
    connecting = 'yellow',
}


/**
 * WebSocketへの接続パネルのパラメタのインターフェース
 */
export interface CtrlWebSocketProps{
    ServerIp : string | undefined;
    PortNo : string | undefined;
    Protocol : string | undefined;
}

/**
 * 設定値 - ネットワーク関連
 */
export interface EnvNetworkManager{
    ws_mode : string | undefined,
    ws_host : string | undefined,
    ws_port : string | undefined,
    ws_protcol : string | undefined,
}


/**
 * 設定値 - コマンド関連
 */
export interface EnvSendCommand{
    type_emergency : string | undefined,
    type_operation : string | undefined,
    type_sound : string | undefined,
}

/**
 * momoサーバへの接続パネルのパラメタのインタフェース
 */
export interface MomoServerProps extends CtrlWebSocketProps{
    DeviceName : string;
    Codec : string;
    Used : boolean;
}

/**
 * 
 * @returns 現在日付
 */
export function DateNow() : string {

    const now = new Date();
  
    // 各部分を取得
    const year = now.getFullYear();
    const month = ('0' + (now.getMonth() + 1)).slice(-2); // 月は0から始まるので+1
    const day = ('0' + now.getDate()).slice(-2);
    const hours = ('0' + now.getHours()).slice(-2);
    const minutes = ('0' + now.getMinutes()).slice(-2);
    const seconds = ('0' + now.getSeconds()).slice(-2);
    const milliseconds = ('00' + now.getMilliseconds()).slice(-3);
  
    // 連結して表示
    return `${year}-${month}-${day}_${hours}:${minutes}:${seconds}.${milliseconds}`;

}

/**
 * ダッシュボードからのパラメタのインターフェース
 */
export interface DashboardContentProps {

    /**
     * ラズパイとの通信用のwebsocket本体
     */
    networkmanager?: NetworkManager | null;

    /**
     * momoのサーバ管理マネージャ
     */
    momomanager?: MomoManager | null;

    /**
     * コマンドを送信するパラメタ関連
     */
    envsendcommand?: EnvSendCommand | null

}
