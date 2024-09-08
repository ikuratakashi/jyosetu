/**
 * @ikuratakashi
 * ログをまとめたクラス
 */
export class UtilsLogger{

    /**
     * ログを出力する
     * @param pMessage 出力するログのメッセージ
     * ```js
     * this.Logger.Log(`${this.Logger.getMethodName()}():data:${event.data}`);
     * ```
     */
    Log(pMessage:string,pValue?:any){
        if(pValue){
            console.log(pMessage,pValue);
        }else{
            console.log(pMessage);
        }
    }

    /**
     * コンソールのグループ開始
     */
    ConsoleGroupSet(){
        console.group();
    }
    
    /**
     * コンソールのグループ終了
     */
    consoleGroupEnd(){
        console.groupEnd();
    }

    /**
     * 
     * @param pErrMsg - エラーメッセージ
     * @param pError  - [?] エラーオブジェクト
     */
    LogError(pErrMsg:string,pError?:any){
        if(pError){
            console.error(pErrMsg,pError);
        }else{
            console.error(pErrMsg);
        }
    }

    /**
     * 現在のメソッド名を取得する
     * @returns メソッド名
     */
    getMethodName() {
        const error = new Error();
        const stack = error.stack ? error.stack.split('\n') : null;
        const methodName = stack ? stack[2].trim().split(' ')[1] : "???????";
        return methodName;
    }
}