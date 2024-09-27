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

## .gitgnoreに除外するファイルを追加しても管理から除外されない場合

キャッシュが有効になっています。

以下のコマンドを実行してキャッシュから削除してください。

キャッシュを削除すると除外が反映されます。

例）

`*.pid`というファイルを除外した場合

```
git rm --cached *.pid
```
