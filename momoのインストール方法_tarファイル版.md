# momoのインストール tar版

ラズパイのCPUに合わせてインストールするmomoが違うので、まずはラズパイのCPUを調べます。

## ラズパイでCPUなどの情報を参照する方法

```bash
vim /proc/cpuinfo 
```
vimはvimエディター。unixなどではスタンダードなテキストエディタです。

以下のように表示されます。
```
processor       : 0
  2 model name      : ARMv7 Processor rev 4 (v7l)
  3 BogoMIPS        : 76.80
  4 Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva     idivt vfpd32 lpae evtstrm crc32
```

vimを終了させるのは、escキーを押して、`:` を押した後に、`q!` と入力してエンターキーを押せば終了します。`q` は終了、`!` は強制的という意味合いです。

## ラズパイ5の場合

ラズパイ5では表示されませんでした。。。
Cpilotに聞いたら、以下の回答をもらいました。

> Raspberry Pi 5のCPUはBroadcom BCM2712というSoCに搭載されており、その中にはArm Cortex-A76が4つ搭載されています。

GitHubにはそのCPUに対応するReleaseは無かったので、以下のものを使用しました。

```
https://github.com/shiguredo/momo/releases/download/2024.1.0/momo-2024.1.0_raspberry-pi-os_armv8.tar.gz
```

## momoのインストール(Armv7用 ラズパイ3など)

Raspberry Pi上で`momo-2023.1.0_raspberry-pi-os_armv7.tar.gz`をダウンロードするには、以下の手順を実行してください：

1. **ターミナルを開く**:
   Raspberry Piのターミナルを開きます。

2. **ファイルをダウンロード**:
   `wget`コマンドを使用してファイルをダウンロードします。
   ```bash
   wget https://github.com/shiguredo/momo/releases/download/2023.1.0/momo-2023.1.0_raspberry-pi-os_armv7.tar.gz
   ```

   ```bash
   wget https://github.com/shiguredo/momo/releases/download/2024.1.0/momo-2024.1.0_raspberry-pi-os_armv8.tar.gz
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

## momoのインストール(Armv8用 ラズパイ5など)

Raspberry Pi上でmomoをダウンロードするには、以下の手順を実行してください：

1. **ターミナルを開く**:

   Raspberry Piのターミナルを開きます。

2. **ファイルをダウンロード**:

   `wget`コマンドを使用してファイルをダウンロードします。
   ```bash
   wget https://github.com/shiguredo/momo/releases/download/2024.1.0/momo-2024.1.0_raspberry-pi-os_armv8.tar.gz
   ```

3. **ファイルの解凍**:

   ダウンロードしたファイルを解凍します。

   ```bash
   tar -zxvf momo-2024.1.0_raspberry-pi-os_armv8.tar.gz
   ```
   解凍されるとコマンドを実行した場所に `momo` フォルダが作成されます。 

4. **ディレクトリの移動**:

   解凍したディレクトリに移動します。

   ```bash
   cd momo
   ```

5. **Momoの実行**:

   Momoを実行してテストモードで動作確認を行います。

   ```bash
   ./momo --no-audio-device test
   ```
   これを実行したら、ブラウザでテスト用のサイトにアクセスします。次の章で説明しています。

6. **Momoの停止**:

   コマンドラインで `Ctrl+C` を押すと、momoが終了します。

7. **Momoの停止 プロセス版**

   `&` などを指定して実行した場合、プロセスとして動作しています。
   それらのプロセスを停止するには、以下のコマンドでプロセスを調べます。

   ```bash
   ps -ef | grep -E 'momo'   
   ```

   コマンドを実行すると以下のように表示されます。

   ```bash
   jyosetu  1232918       1  0 08:21 pts/3    00:00:00 ./momo --no-audio-device test
   jyosetu  1233959  960285  0 08:22 pts/3    00:00:00 grep --color=auto -E momo
   ```

   jyosetに続く番号がプロセスIDです。以下のコマンドでプロセスを停止します。

   ```bash
   kill 1232918
   ```

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

   例: Raspberry Piのホスト名が`jyosetu2`の場合、
   ```
   http://jyosetu2.local:8080/html/test.html
   ```

5. **Codecの選択**:

   test.htmlの一番左側のリストボックスで、`H264` 以外を選択してください。
   
   ラズパイ5では `H264` は使えません。

4. **Connectボタンを押す**:

   ページが表示されたら、`Connect`ボタンを押します。これでRaspberry Piからの映像がブラウザに表示されます。

これで映像を確認できます。

## フォルダの削除方法

```bash
sudo rm -r フォルダ名
```