# React

## 静的なhtmlを作成する方法

momoを起動した時にサイトを表示させるために、静的なhtmlなどを生成する必要があります。
以下のコマンドで`build`フォルダに生成されます。
```
yarn run build
```
`build` フォルダの内容を `html` にコピーし、momoを起動すると、htmlフォルダ内のファイルを読み込んでサイトが表示できるようになります。

## buildをした時に自動でbuildの内容をgh-pagesブランチへpushする方法

https://emit.hateblo.jp/entry/2023/08/26/163533

この方法の時に、`package.json` と ~~`src\dashboard\Dashboard.tsx`~~ を変更する内容

- package.json 追加文字列
```
  "homepage": ".",
```

- Dashboard.tsx の変更内容
```
```

※これでもうまくいかない。。。

## リポジトリをクローンした後に実行するコマンド

`yarn run build` を実行した時に、以下のエラーが表示された。

```
yarn run v1.22.22
$ react-scripts build
'react-scripts' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
error Command failed with exit code 1.
info Visit https://yarnpkg.com/en/docs/cli/run for documentation about this command.
```

これの解決方法をAIに聞いた結果が以下の通り。

---
このエラーメッセージは、`react-scripts`がインストールされていないか、正しく認識されていないことが原因です。以下の手順で問題を解決できます：

1. **`react-scripts`をインストールする**:
   - プロジェクトのルートディレクトリで以下のコマンドを実行して、`react-scripts`をインストールします。
     ```bash
     npm install react-scripts --save
     ```

2. **依存関係を再インストールする**:
   - 依存関係が正しくインストールされていない可能性があるため、以下のコマンドで依存関係を再インストールします。
     ```bash
     rm -rf node_modules
     rm yarn.lock
     yarn install
     ```

3. **`package.json`の確認**:
   - `package.json`に`react-scripts`が依存関係として含まれているか確認します。以下のように記載されているはずです。
     ```json
     "dependencies": {
       "react": "^17.0.2",
       "react-dom": "^17.0.2",
       "react-scripts": "5.0.1"
     }
     ```

4. **Node.jsのバージョンを確認する**:
   - Node.jsのバージョンが古い場合、最新の安定版にアップデートしてみてください。特に、Node.js v17以上を使用している場合は、以下の環境変数を設定してからビルドを試みてください。
     ```bash
     export NODE_OPTIONS=--openssl-legacy-provider
     yarn run build
     ```

これらの手順を試してみて、再度`yarn run build`を実行してみてください。問題が解決しない場合は、エラーメッセージの詳細を教えていただければ、さらにサポートいたします。何か他に質問があれば教えてくださいね。¹²³

ソース: Copilot との会話、 2024/8/26
(1) [FAQ] 「'react-scripts' は、内部コマンドまたは外部コマンド .... https://qiita.com/kishiro/items/cfd2bfe83f461b08588a.
(2) Node.jsとyarnでのReactアプリ開発中に発生したエラーの解決 .... https://zenn.dev/meg_zenn/articles/nodejs-yarn-react-error-solution.
(3) [Node][Yarn] create-react-app したプロジェクトでyarn start でエラー. https://qiita.com/sachiotomita/items/407a3cb6a285bf2e6d62.
(4) Fixing 'react-scripts' is not recognized error | sebhastian. https://sebhastian.com/react-scripts-not-recognized-fix/.
(5) Troubleshooting | Create React App. https://create-react-app.dev/docs/troubleshooting/.
(6) undefined. http://yarnpkg.com/%29.
