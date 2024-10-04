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

## React - Material Icons

Material Iconsで検索を行いたい場合は、以下のサイトで検索する

https://mui.com/material-ui/material-icons/

## ソース内で特定のファイル（画像など）を参照したい場合

publicフォルダにファイルを設置します。

例）
```
public
 └ doc
    └ ラズパイサーバの使い方.md
```

ソース内での参照は以下の通り。

```
const markdownUrl = process.env.PUBLIC_URL + '/doc/ラズパイサーバの使い方.md';
```

# React コード補完

VSCodeでReact開発を行う際に、コード補完やスニペットを自動的に提供してくれる機能があります。これらの機能を利用することで、効率的にコーディングができます。以下に、いくつかの基本的なスニペットやコード補完の例を示します。

* **インストールが必要な拡張機能**
  ```
  ES7+ React/Redux/React-Native snippets
  ```

### 基本的なスニペット
1. **`rfc`**:
   - React Functional Componentのテンプレートを生成します。
   ```javascript
   import React from 'react';

   const ComponentName = () => {
       return (
           <div>
               
           </div>
       );
   }

   export default ComponentName;
   ```

2. **`rcc`**:
   - React Class Componentのテンプレートを生成します。
   ```javascript
   import React, { Component } from 'react';

   class ComponentName extends Component {
       render() {
           return (
               <div>
                   
               </div>
           );
       }
   }

   export default ComponentName;
   ```

3. **`useState`**:
   - `useState`フックのテンプレートを生成します。
   ```javascript
   const [state, setState] = useState(initialState);
   ```

4. **`useEffect`**:
   - `useEffect`フックのテンプレートを生成します。
   ```javascript
   useEffect(() => {
       // Effect
       return () => {
           // Cleanup
       };
   }, [dependencies]);
   ```

### 拡張機能の利用
VSCodeには、React開発を支援するための拡張機能が多数あります。以下の拡張機能をインストールすると、さらに便利になります。

1. **ES7+ React/Redux/React-Native snippets**:
   - 上記のスニペットを含む多くのスニペットを提供します。
   - インストール後、`rfc`や`rcc`などのショートカットを使用できます。

2. **Prettier - Code formatter**:
   - コードのフォーマットを自動的に整えてくれます。

3. **ESLint**:
   - コードの品質を保つためのLintingツールです。

これらのスニペットや拡張機能を活用することで、React開発がよりスムーズになります。何か他にご質問があれば、お気軽にどうぞ！