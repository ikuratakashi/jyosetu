
class clsSendMessage{
    constructor(pWsUri){
        this.wsuri = pWsUri;
    }
}
function OnLoad(){
    let WsUri = document.getElementById("ws_uri").value
    const SendMsg = new clsSendMessage(WsUri)
}
