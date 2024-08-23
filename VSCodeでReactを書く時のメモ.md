# VSCodeでReactを書く時のメモ

## コンポーネントファイルを作成するときの補完

- rfce

基本のソースを作ってくれる

以下のソースが生成される。`CtrlClutchAccel`の部分はファイル名になる。
```
import React from 'react'

function CtrlClutchAccel() {
  return (
    <div>
      
    </div>
  )
}

export default CtrlClutchAccel
```

## Material Icons

- アイコンの一覧URL
https://mui.com/material-ui/material-icons/

- 丸付きUP、Down
```
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
```