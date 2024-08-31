import React, { useState } from 'react';
import { Button } from '@mui/material';
import { CleateJsonActionToStr } from '../utils/UtilsJson';
import * as UtilsCommon from '../utils/UtilsCommon';

/**
 * ボタンの引数のインターフェース
 */
export interface UtilsButtonProps {
    sx?: object;
    props: any;
    ButtonType: UtilsCommon.enmButtonType;
    children : React.ReactNode;
}

/**
 *  ボタンを押し続けたときのメッセージを送信する時間間隔
 */
const IntervalMs = 100;

/**
 * ボタン
 * 
 * @param sx - デザインパラメタ
 * @param props - props
 * @param ButtonType - ボタンの種類
 * @returns 
 */
const UtilsButton: React.FC<UtilsButtonProps> = ({props, ButtonType, children}) => {

    const {sendMessage} = props;
    const [intervalId, setIntervalId] = useState<number | null>(null);;

    /**
     * タイマーの起動
     * 一定間隔でメッセージをサーバに送る
     */
    const startInterval = () =>{
        const id = setInterval
                    (
                        () => {
                            sendMessage(CleateJsonActionToStr(ButtonType,1));
                        }
                        , IntervalMs
                    );
                    
        setIntervalId(id as unknown as number);
    }

    /**
     * マウスをクリックしたときのイベント
     * サーバへ、ボタンを押したときのメッセージを送信する
     */
    const onMouseClick = () =>{
        sendMessage(CleateJsonActionToStr(ButtonType,1));
    }

    /**
     * マウスを押した時のイベント
     * サーバへ、ボタンを押している事を一定間隔で送信する
     */
    const onMouseDown = () =>{
        startInterval();
    }

    /**
     * タイマーの停止
     */
    const stopInterval = () => {
        clearInterval(intervalId as unknown as number);
    };

    /**
     * マウスを離したときの処理
     * サーバへ送信しているメッセージの送信を停止する
     */
    const onMouseUp = () => {
        stopInterval();
    }

    /**
     * マウスを離したときの処理
     * サーバへ送信しているメッセージの送信を停止する
     */
    const onMouseLeave = () => {
        stopInterval();
    }

    return (
        <Button 
            {...props} 
            onClick={onMouseClick}
            onMouseDown={onMouseDown}
            onMouseUp={onMouseUp}
            onMouseLeave={onMouseUp}
            onTouchStart={onMouseDown}
            onTouchEnd={onMouseUp}
            onTouchCancel={onMouseUp}
        >
            {children}
        </Button>
    );
};

export default UtilsButton;
