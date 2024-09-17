# Git のメモ

## pushしたらエラーが出た時の対応方法

### エラー内容
```
error: https://github.com/ikuratakashi/jyosetu.git did not send all necessary objects
```

### 対応内容

1. ファイルを削除
```
.git/refs/remotes/origin/develop-ikura
```

2. fetchを行う
```
git fetch origin
```

3. pushを行う
```
git push origin develop-ikura
```
以下の結果が表示されればOK
```
Everything up-to-date
```

