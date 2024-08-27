import React, { useState, useEffect, useRef } from 'react';
import DashboardContent from './dashboard/Dashboard';

const App = () => {

  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState<string>('');
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // WebSocket接続を確立
    const socket = new WebSocket('ws://192.168.3.10:1000');
    socketRef.current = socket;

    // サーバーからメッセージを受信
    socket.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    // エラーハンドリング
    socket.onerror = (error) => {
      console.error('WebSocket error: ', error);
    };

    // コンポーネントがアンマウントされた時にWebSocketを閉じる
    return () => {
      socket.close();
    };

  }, []);

  const sendMessage = (message: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(message);
      setInput('');
    } else {
      console.error("WebSocket is not open or is null.");
    }
  };

  return <DashboardContent sendMessage={sendMessage}/>;

};

export default App;