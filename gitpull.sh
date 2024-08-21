#!/bin/bash
git branch
echo "現在のブランチにdevelop-ikuraを強制的に上書きします。"
echo "よろしいですか？ (y/n)"
read answer

if [ "$answer" = "y" ]; then
    git fetch origin
    git reset --hard origin/develop-ikura
    chmod 777 ./html/init.sh
else
    echo "処理を中止しました。"
    exit
fi

echo "続けてmomoなどを実行できるように設定します。"
echo "よろしいですか？ (y/n)"
read answer

if [ "$answer" = "y" ]; then
    cd html
    ./init.sh
    cd ..
else
    echo "処理を中止しました。"
    exit
fi

