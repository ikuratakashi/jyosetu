/**
 * @ikuratakashi
 * 共通モジュール
 */
 import { CleateJsonActionToStr } from './UtilsJson';

/**
 * ダッシュボードからのパラメタのインタフェース
 */
export interface DashboardContentProps {

    /**
     * websocketへ送信する
     * @param message 送信するメッセージ
     * @returns void
     */
    sendMessage: (message: string) => void;

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
    move_up     = 'move_up',
    /**
    * 移動 後進
    */
    move_dw     = 'move_dw',
    /**
    * 移動 右
    */
    move_right  = 'move_right',
    /**
    * 移動 左
    */
    move_left   = 'move_left',
    /**
    * 雪射出口 上向き
    */
    chute_up    = 'chute_up',
    /**
    * 雪射出口 下向き
    */
    chute_dw    = 'chute_dw',
    /**
    * 雪射出口 左向き
    */
    chute_left  = 'chute_left',
    /**
    * 雪射出口 右向き
    */
    chute_right = 'chute_right',
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

