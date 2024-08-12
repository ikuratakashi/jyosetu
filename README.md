# jyosetu

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