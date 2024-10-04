import React, { useState, useEffect  } from 'react'
import {Button, Grid} from '@mui/material';
import * as UtilsCommon from '../utils/UtilsCommon'

export default function CtrlResponse(props: UtilsCommon.DashboardContentProps) {

    const [message, setMessage] = useState('');
    useEffect(() => {
        // ここで値を設定するタイミングを制御します
        // 例えば、サーバーからのメッセージを取得する場合
        const fetchMessage = async () => {
        // サーバーからメッセージを取得するロジックをここに記述
        const serverMessage = "This is a message from the server.";
        setMessage(serverMessage);
        };

        fetchMessage();
    }, []); // 空の依存配列を渡すことで、コンポーネントのマウント時に一度だけ実行されます

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <label htmlFor="readonly-input">Server Message</label>
            <div style={{ width: '100%', height: '100%' }}>
                <textarea
                    readOnly
                    value={message}
                    style={{ 
                        width: '100%', 
                        height: '100%', 
                        textAlign: 'left', // 左寄せ
                        verticalAlign: 'top', // 上寄せ
                        resize: 'none' // サイズ変更を無効にする
                    }}
                >
                </textarea>
            </div>
        </div>
    )
}
