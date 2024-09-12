// utils/convertToJson.js
export function CleateJsonActionToStr(button, value) {

    // 現在時刻を取得
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // 月は0から始まるので+1します
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const milliseconds = String(now.getMilliseconds()).padStart(3, '0'); // ミリ秒は3桁

    return JSON.stringify(
        {
            "action":
            [
                { 
                    "type":"OPERATION",
                    "button":button, 
                    "value":value,
                    "time":`${year}/${month}/${day} ${hours}:${minutes}:${seconds}:${milliseconds}`
                }
            ]
        }
    );
}
