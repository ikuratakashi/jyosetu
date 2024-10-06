# momoの使い方

## テスト方法

[momoのインストール方法_tarファイル版.md](./momoのインストール方法_tarファイル版.md) の `momoの動作確認` を参照してください。

## デバイス名などを指定して起動する方法

新しいバージョンから、デバイス名を指定する時に `/dev/video0` などで指定することができなくなりました。`usb-xhci-hcd.1-1.2.1` などの名前で指定します。


**デバイス名を指定してmomoを起動するコマンドは以下の通りです。**

```bash
./momo --no-audio-device --video-device "usb-xhci-hcd.1-1.2.1" test
```

デバイス名を取得するには以下のコマンドを実行してください。

```bash
v4l2-ctl --list-devices | grep 'Camera'
```

実行結果

```bash
HD USB Camera: USB Camera (usb-xhci-hcd.1-1.2.1):
HD USB Camera: USB Camera (usb-xhci-hcd.1-1.2.2):
HD USB Camera: USB Camera (usb-xhci-hcd.1-1.2.3):
HD USB Camera: USB Camera (usb-xhci-hcd.1-1.2.4):
UVC Camera (046d:0825) (usb-xhci-hcd.1-1.4):
```

各行の最後の `()` 部分が、指定するデバイス名です。

以下のコマンドだと、デバイス名だけを表示します。

```bash
sudo v4l2-ctl --list-devices | grep 'Camera' | sed -n 's/.*(\([^):]*\)).*/\1/p'
```

実行結果

```bash
usb-xhci-hcd.1-1.2.1
usb-xhci-hcd.1-1.2.2
usb-xhci-hcd.1-1.2.3
usb-xhci-hcd.1-1.2.4
usb-xhci-hcd.1-1.4
```

以前のバージョンだと `/dev/video0` の指定でしたが、momoで使えるデバイスかどうかは `v4l2-ctl --device=/dev/video0 --all` などを実行して更に調べる必要があったので、この方法になったのだと思います。

## momoをプロセスとして起動する方法

コマンドの最後に `&` をつけるとプロセスとして実行されます。

```bash
./momo --no-audio-device --video-device "usb-xhci-hcd.1-1.2.1" test &
```


### Momoの停止 プロセス版

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
