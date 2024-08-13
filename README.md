# jyosetu

ある機構を遠隔操作するために、ラズパイについたカメラの画像を[momo](https://momo.shiguredo.jp/)で映像をブラウザで受信しながら、WebSocketsを使ってメッセージを送って、機構を操作するプログラム群です。

## システム構成について

- momoサーバ
- メッセージ受信用のWebSocketsのサーバ

ラズパイから先にはPLCが付いているので、ラズパイからは制御信号のみ送信します。

## momoのダウンロードについて

githubよりmomoのバイナリがダウンロードできます。

https://github.com/shiguredo/momo/releases

テスト用のラズパイはプロセッサが`ARMv7`だったので、以下をダウンロードしました。

https://github.com/shiguredo/momo/releases/download/2023.1.0/momo-2023.1.0_raspberry-pi-os_armv7.tar.gz

- ダウンロード
```bash
wget https://github.com/shiguredo/momo/releases/download/2023.1.0/momo-2023.1.0_raspberry-pi-os_armv7.tar.gz
```

- 解凍
```bash
tar -zxvf momo-2023.1.0_raspberry-pi-os_armv7.tar.gz
```

あとは、解凍したフォルダから、`momo` 本体と `html` フォルダを実行環境へコピーしました。

# momoの起動について

## momo自体の実行権限の付与

```bash
chmod 770 momo
```

## その他の権限付与
※クローンした状態だと、色々なファイルやディレクトリに権限が当たっていないので、以下のコマンドで実行権限を与えてください。

```bash
chmod 774 momo_st.sh
```
```bash
chmod 774 momo_ed.sh
```
```bash
chmod 770 tmp
```

## 起動方法
```bash
./momo_st.sh
```

実行するとたまに`failed to create capturer`というメッセージが表示されて、キー入力をしないと進みません。

momoがラズパイ上でカメラから映像をキャプチャできなかった時のメッセージのようですが、これが出ても、momoのサーバが立って、動画は配信されるので、よくわかりません。

これが出てもエンターキーを押してもmomoは起動しているので大丈夫です。

## 終了方法
```bash
./momo_ed.sh
```

## ブラウザでの表示
他の端末などで、以下のURLを表示すると、サイトが表示されると思います。

`http://<momoが起動しているhostのIP>/html/text.html`

このサイトの`Connect`ボタンをクリックするとカメラ映像が表示されます。

PlayとSendについては、押しても何も動かないです。momoのマニュアルか何かには書いてあるかもしれません。

# ラズパイの環境設定

## vncの設定
1. 左上のラズパイマーク
2. 設定
3. Raspberry Pi の設定
4. インターフェイス
5. VNCのチェックをONにする

# ラズパイコマンド

## CPUなどの情報を参照する方法
```bash
vim /proc/cpuinfo 
```
以下のように表示される
```
processor       : 0
  2 model name      : ARMv7 Processor rev 4 (v7l)
  3 BogoMIPS        : 76.80
  4 Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva     idivt vfpd32 lpae evtstrm crc32
  ```