# momoのインストール tar版

## フォルダの削除方法

```bash
sudo rm -r フォルダ名
```

## momoのインストール

Raspberry Pi上で`momo-2023.1.0_raspberry-pi-os_armv7.tar.gz`をダウンロードするには、以下の手順を実行してください：

1. **ターミナルを開く**:
   Raspberry Piのターミナルを開きます。

2. **ファイルをダウンロード**:
   `wget`コマンドを使用してファイルをダウンロードします。
   ```bash
   wget https://github.com/shiguredo/momo/releases/download/2023.1.0/momo-2023.1.0_raspberry-pi-os_armv7.tar.gz
   ```

3. **ファイルの解凍**:
   ダウンロードしたファイルを解凍します。
   ```bash
   tar -zxvf momo-2023.1.0_raspberry-pi-os_armv7.tar.gz
   ```

4. **ディレクトリの移動**:
   解凍したディレクトリに移動します。
   ```bash
   cd momo-2023.1.0_raspberry-pi-os_armv7
   ```

5. **Momoの実行**:
   Momoを実行してテストモードで動作確認を行います。
   ```bash
   ./momo --no-audio-device test
   ```

これでMomoを使ったWebRTCのテスト配信ができるはずです。何か他にお手伝いできることがあれば教えてくださいね。

ソース: Copilot との会話、 2024/8/12
(1) WebRTC Native Client Momo - shiguredo.jp. https://momo.shiguredo.jp/.
(2) Releases · shiguredo/momo · GitHub. https://github.com/shiguredo/momo/releases.
(3) Momoを使ってRaspberry Pi 映像のリアルタイム配信 - Qiita. https://qiita.com/northarant/items/7b97799e15b18b5b0c76.
(4) WebRTC Native Client Momoの低遅延配信を Raspi 4 でためす .... https://qiita.com/Ninagawa123/items/88460922abb04a82c220.
(5) undefined. https://github.com/shiguredo/momo/releases/download/2022.1.0/momo-2022.1.0_raspberry-pi-os_armv7.tar.gz.
(6) undefined. https://github.com/shiguredo/momo/releases/download/2021.2.3/momo-2021.2.3_raspberry-pi-os_armv7.tar.gz.

## momoの動作確認
Momoを実行した後、映像を確認するための手順は以下の通りです：

1. **Raspberry PiのIPアドレスを確認**:
   ターミナルで以下のコマンドを実行して、Raspberry PiのIPアドレスを確認します。
   ```bash
   hostname -I
   ```

2. **ブラウザを開く**:
   同じネットワークに接続されているPCやスマートフォンのブラウザを開きます。

3. **URLにアクセス**:
   ブラウザのアドレスバーに以下のURLを入力します。
   ```
   http://<Raspberry PiのIPアドレス>:8080/html/test.html
   ```
   例: Raspberry PiのIPアドレスが`192.168.1.100`の場合、
   ```
   http://192.168.1.100:8080/html/test.html
   ```

4. **Connectボタンを押す**:
   ページが表示されたら、`Connect`ボタンを押します。これでRaspberry Piからの映像がブラウザに表示されます。

これで映像を確認できるはずです。何か他にご質問やお手伝いできることがあれば教えてくださいね。