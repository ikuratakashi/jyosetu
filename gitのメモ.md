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
## VSCodeでGitHubと同期を取ろうとしたらエラーが表示された場合

以下のメッセージが出た場合
```bash
error: object file .git/objects/64/c022655ec25579d540376c4883bbb1efcf3e42 is empty
```

1. .gitのバックアップを作成

```bash
cp -a .git .git-old
```

2. 空のファイルを削除

```bash
cd .git/
find . -type f -empty -delete -print
```

3. 全てのファイルが正しく処理されたか確認

```bash
git fsck --full
git gc --prune=now
```

コマンドを入力したら、2分くらい待ちます。以下のようなメッセージが表示されます。
```bash
Checking object directories: 100% (256/256), done.
Checking objects: 100% (1912/1912), done.
error: refs/remotes/origin/develop-ikura: invalid sha1 pointer 64c022655ec25579d540376c4883bbb1efcf3e42
error: refs/remotes/origin/develop-ikura: invalid reflog entry 64c022655ec25579d540376c4883bbb1efcf3e42
dangling commit d7d818f47db5d9699c64e1b3a1414d7a9631bdd7
error: refs/remotes/origin/develop-ikura does not point to a valid object!
error: Could not read 64c022655ec25579d540376c4883bbb1efcf3e42
fatal: bad object refs/remotes/origin/develop-ikura
fatal: failed to run repack
```