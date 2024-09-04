import React, { useState, useRef, useEffect} from 'react';
import { Button } from '@mui/material';
import { CleateJsonActionToStr } from '../utils/UtilsJson';
import * as UtilsCommon from '../utils/UtilsCommon';
import { useGamepad } from './useGamepad';
import * as UtilsNetworkManager from './UtilsNetworkManager';

/**
 * ボタンの引数のインターフェース
 */
export interface UtilsButtonProps {
    sx?: object;
    variant?:string;
    startIcon?:any;
    props: any & UtilsCommon.DashboardContentProps;
    ButtonType: UtilsCommon.enmButtonType;
    children : React.ReactNode;
}

/**
 *  ボタンを押し続けたときのメッセージを送信する時間間隔
 */
const IntervalMs = 200;

/**
 * ボタン
 * 
 * @param sx - デザインパラメタ
 * @param props - props
 * @param ButtonType - ボタンの種類
 * @returns 
 */
const UtilsButton: React.FC<UtilsButtonProps> = ({
    sx,
    variant,
    startIcon,
    props,
    ButtonType,
    children,
}) => {

    let left = false, up = false, right = false, down = false, buttonA = false, buttonB = false, buttonX = false, buttonY = false, LB = false, LT = false, RB = false, RT = false, start = false;
    let joystick: number[] = [0, 0], joystickRight: number[] = [0, 0];

    try {
        const gamepadState = useGamepad() || {};
        if (gamepadState) {
            left = gamepadState.left ?? false;
            up = gamepadState.up ?? false;
            right = gamepadState.right ?? false;
            down = gamepadState.down ?? false;
            buttonA = gamepadState.buttonA ?? false;
            buttonB = gamepadState.buttonB ?? false;
            buttonX = gamepadState.buttonX ?? false;
            buttonY = gamepadState.buttonY ?? false;
            LB = gamepadState.LB ?? false;
            LT = gamepadState.LT ?? false;
            RB = gamepadState.RB ?? false;
            RT = gamepadState.RT ?? false;
            start = gamepadState.start ?? false;
            joystick = gamepadState.joystick ?? [0, 0];
            joystickRight = gamepadState.joystickRight ?? [0, 0];
        } 
    } catch (error) {
    }
    
    const {networkmanager}: { networkmanager: UtilsNetworkManager.NetworkManager} = props;
    const NetworkManager = networkmanager;
    const [intervalId, setIntervalId] = useState<number | null>(null);;

    /**
     * タイマーの起動
     * 一定間隔でメッセージをサーバに送る
     */
    const startInterval = () =>{
        const id = setInterval
                    (
                        () => {
                            if (NetworkManager){
                                NetworkManager.sendWsMessage(CleateJsonActionToStr(ButtonType,1));
                            } 
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
        if (NetworkManager){
            NetworkManager.sendWsMessage(CleateJsonActionToStr(ButtonType,1));
        } 
        //sendMessage(CleateJsonActionToStr(ButtonType,1));
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

    /**
     * コントローラのボタンと画面上のボタンの割り当て
     */
    let setButton: boolean | undefined = false;
    switch(ButtonType){
        case UtilsCommon.enmButtonType.clutch_up:
            setButton = LB;
            break;
        case UtilsCommon.enmButtonType.clutch_dw:
            setButton = LT;
            break;
        case UtilsCommon.enmButtonType.accel_up:
            setButton = RB;
            break;
        case UtilsCommon.enmButtonType.accel_dw:
            setButton = RT;
            break;
        case UtilsCommon.enmButtonType.move_fw:
            setButton = up;
            break;
        case UtilsCommon.enmButtonType.move_bk:
            setButton = down;
            break;
        case UtilsCommon.enmButtonType.move_left:
            setButton = left;
            break;
        case UtilsCommon.enmButtonType.move_right:
            setButton = right;
            break;
        case UtilsCommon.enmButtonType.chute_L_up:
            //左ジョイスティック　↑
            if(-0.5 <= joystick[0] && joystick[0] < 0.5 && -1 == joystick[1]    ){

                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_rup:
            //左ジョイスティック　↗
            if(0.5 <= joystick[0] && joystick[0] <= 1 && -1 <= joystick[1] && joystick[1] < -0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_right:
            //左ジョイスティック　→
            if(1 == joystick[0]     && -0.5 <= joystick[1] && joystick[1] < 0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_rdw:
            //左ジョイスティック　↘
            if(0.5 <= joystick[0] && joystick[0] <= 1 && 0.5 <= joystick[1] && joystick[1] <= 1){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_dw:
            //左ジョイスティック　↓
            if(-0.5 <= joystick[0] && joystick[0] < 0.5 && 1 == joystick[1]    ){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_ldw:
            //左ジョイスティック　↙
            if(-1 <= joystick[0] && joystick[0] < -0.5 && 0.5 <= joystick[1] && joystick[1] <= 1){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_left:
            //左ジョイスティック　←
            if(-1 == joystick[0]     && -0.5 <= joystick[1] && joystick[1] < 0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_L_lup:
            //左ジョイスティック　↖
            if(-1 <= joystick[0] && joystick[0] < -0.5 && -1 <= joystick[1] && joystick[1] <= -0.5){
                setButton = true;
            }
            break;

        case UtilsCommon.enmButtonType.chute_R_up:
            //右ジョイスティック　↑
            if(-0.5 <= joystickRight[0] && joystickRight[0] < 0.5 && -1 == joystickRight[1]    ){
        
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_rup:
            //右ジョイスティック　↗
            if(0.5 <= joystickRight[0] && joystickRight[0] <= 1 && -1 <= joystickRight[1] && joystickRight[1] < -0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_right:
            //右ジョイスティック　→
            if(1 == joystickRight[0]     && -0.5 <= joystickRight[1] && joystickRight[1] < 0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_rdw:
            //右ジョイスティック　↘
            if(0.5 <= joystickRight[0] && joystickRight[0] <= 1 && 0.5 <= joystickRight[1] && joystickRight[1] <= 1){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_dw:
            //右ジョイスティック　↓
            if(-0.5 <= joystickRight[0] && joystickRight[0] < 0.5 && 1 == joystickRight[1]    ){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_ldw:
            //右ジョイスティック　↙
            if(-1 <= joystickRight[0] && joystickRight[0] < -0.5 && 0.5 <= joystickRight[1] && joystickRight[1] <= 1){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_left:
            //右ジョイスティック　←
            if(-1 == joystickRight[0]     && -0.5 <= joystickRight[1] && joystickRight[1] < 0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.chute_R_lup:
            //右ジョイスティック　↖
            if(-1 <= joystickRight[0] && joystickRight[0] < -0.5 && -1 <= joystickRight[1] && joystickRight[1] <= -0.5){
                setButton = true;
            }
            break;
        case UtilsCommon.enmButtonType.btn_sankaku:
            setButton = buttonY;
            break;
        case UtilsCommon.enmButtonType.btn_sikaku:
            setButton = buttonX;
            break;
        case UtilsCommon.enmButtonType.btn_on:
            setButton = buttonB;
            break;
        case UtilsCommon.enmButtonType.btn_off:
            setButton = buttonA;
            break;
        case UtilsCommon.enmButtonType.btn_em:
            setButton = start;
            break;
        }

    /**
     * コントローラーのボタンを押した時のイベントを設定
     */
    const SetRef = useRef<HTMLButtonElement>(null);
    React.useEffect(() => 
    {
        if (setButton && SetRef.current) {

            const mouseDownEvent = new MouseEvent('mousedown', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            SetRef.current.dispatchEvent(mouseDownEvent);

            const ClickEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            SetRef.current.dispatchEvent(ClickEvent);
        }

        if (setButton == false && SetRef.current) {
            const mouseUpEvent = new MouseEvent('mouseup', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            SetRef.current.dispatchEvent(mouseUpEvent);
        }

    }, [setButton]);

    return (
        <Button 
            sx = {sx}
            variant = {variant}
            startIcon = {startIcon}
            {...props} 
            onClick = {onMouseClick}
            onMouseDown = {onMouseDown}
            onMouseUp = {onMouseUp}
            onMouseLeave = {onMouseUp}
            onTouchStart = {onMouseDown}
            onTouchEnd = {onMouseUp}
            onTouchCancel = {onMouseUp}
            ref={SetRef}
        >
            {children}
        </Button>
    );
};

export default UtilsButton;
