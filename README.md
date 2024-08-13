# jyosetu

ある機構を遠隔操作するために、ラズパイについたカメラの画像を[momo](https://momo.shiguredo.jp/)で映像をブラウザで受信しながら、websocketsを使ってメッセージを送って機構を操作するプログラム群です。

## システム構成について

- momoサーバ
- メッセージ受信用のwebsocketsのサーバ

ラズパイから先にはPLCが付いているので、


# momoの起動について

## 起動方法
```bash
momo_st.sh
```

## 終了方法
```bash
momo_ed.sh
```

※クローンした状態だと、実行と終了用のシェルに実行権限が当たっていないので、以下のコマンドで実行権限を与えてください。

```bash
sudo chmod 774 momo_st.sh
```
```bash
sudo chmod 774 momo_ed.sh
```

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