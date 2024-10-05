# Pythonメモ

## sudoでプログラムを実行したときにpyenvの環境のPythonが実行されない問題

例えば以下のコマンドでプログラムを実行したときに、pyenvの環境で実行されません。
```
sudo python sv.py
```

sudoで実行した場合、pyenvの環境外で実行されてしまいます。

なので、pyenvの環境でインストールしたライブラリなどが読み込まれません。

以下の対応で解消できます。

1. **ソースの先頭に以下を追加**
    ```
    #!/home/jyosetu/.pyenv/shims/python
    ```

    `jyosetu` の部分は、環境によって変更します。

2. **実行するプログラムに実行権限を与える**

    例）
    ```
    chmod 777 sv.py
    ```

上記の操作を行うことで、`sv.py` を実行したときに pyenvの環境を考慮して実行されます。

実行例）
```
./sv.py
```

## ラズベリーパイ5でのGPIOの利用について

GPIOを利用するためのライブラリがこれまでのものが使えません。

以下のものを試しましたがエラーになりました。

* RPi.GPIO 
* gpiozero

`gpiod`が使えたので、利用について記載します。

## gpiodの利用について

詳しい使い方は [公式サイト](https://pypi.org/project/gpiod/) を参照してください。

### インストール方法
```
pip install gpiod
```

### サンプルソース

LINEに設定している値がGPIOの番号です。

```Python

    # GPIOラインの設定
    LINE = 15
    gpiod.Chip('/dev/gpiochip0').close()
    GPIOLineAct = gpiod.request_lines(
        '/dev/gpiochip0',
        consumer="LED",
        config={
            LINE : gpiod.LineSettings(
                direction=gpiod.line.Direction.OUTPUT,
                output_value=gpiod.line.Value.INACTIVE
            )
        })
        
    #点灯
    GPIOLineAct.set_value(LINE,gpiod.line.Value.ACTIVE)

    #消灯
    GPIOLineAct.set_value(LINE,gpiod.line.Value.INACTIVE)

```

### gpiodで使用するGPIOの番号について
gpiodで使用する番号は、正しくはGPIOの番号ではなく、対応している番号があるのでそれを指定します。

対応表の表示方法は以下のコマンドです。

```bash
gpioinfo
```

コマンドを実行すると以下のような一覧が表示されます。

この一覧表の `line` に続く値が、gpiodで指定する番号になります。

```bash
gpiochip0 - 54 lines:
        line   0:     "ID_SDA"       unused   input  active-high 
        line   1:     "ID_SCL"       unused   input  active-high 
        line   2:      "GPIO2"       unused   input  active-high 
        line   3:      "GPIO3"       unused   input  active-high 
        line   4:      "GPIO4"       unused   input  active-high 
        line   5:      "GPIO5"       unused   input  active-high 
        line   6:      "GPIO6"       unused   input  active-high 
        line   7:      "GPIO7"   "spi0 CS1"  output   active-low [used]
        line   8:      "GPIO8"   "spi0 CS0"  output   active-low [used]
        line   9:      "GPIO9"       unused   input  active-high 
        line  10:     "GPIO10"       unused   input  active-high 
        line  11:     "GPIO11"       unused   input  active-high 
        line  12:     "GPIO12"       unused   input  active-high 
        line  13:     "GPIO13"       unused   input  active-high 
    ：
    ：
```
