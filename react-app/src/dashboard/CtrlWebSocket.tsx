import React, { useState, useEffect  } from 'react'
import {Box, Button, Grid} from '@mui/material';
import {CtrlWebSocketProps} from '../utils/UtilsNetworkManager'
import { Height } from '@mui/icons-material';
import {enmConnectCorlor} from '../utils/UtilsCommon'
import * as UtilsCommon from '../utils/UtilsCommon'


function CtrlWebSocket(props: UtilsCommon.DashboardContentProps) {

    const{networkmanager} = props;
    const NetWorkManager = networkmanager;

    const ButtonSx = {
        fontSize: "11px",
        fontFamily: 'Courier New, monospace',
        borderRadius: 0.5,
        height: '30px',
        width: '40px',
        textAlign: 'center',
        padding: '0px',
        minWidth: '0px',
        color:"white",
        backgroundColor:'gray',
        '&:hover': {
          backgroundColor: 'gray',
          filter: 'brightness(0.8)',
          border:'none',
        },
      };

    const GridSx ={
        border:'0px solid black'
    }
    
    const [wsUri, setWsUri] = useState('');

    useEffect(() => {
        if (NetWorkManager?.WsUri) {
            setWsUri(NetWorkManager.WsUri);
        }
    }, [NetWorkManager]);

    //txtWsUriの値に変更があった時の処理
    const handleChange_txtWsUri = (event:any) => {
        setWsUri(event.target.value);
    };

    //接続ボタンのクリック時の処理
    const handleOnClick_btnConnection = (event:any) =>{
        if(conIsConnection == true){
            //切断
            NetWorkManager?.CloseWsConnect();
        }else{
            //接続
            NetWorkManager?.SocketServerDataParsSet(wsUri);
            NetWorkManager?.ConnectWs();
        }
    }

    //useState
    const [bgColor,setBgColor] = useState(enmConnectCorlor.disconnect);
    const [conMessage,setConnectMessage] = useState('Connect None');
    const [conButton,setConnectButton] = useState({title:'接続',enable:true});
    const [conIsConnection,setIsConnection] = useState(false);

    if(NetWorkManager){
   
        //接続中
        NetWorkManager.onWsOpenConnectingEx = () =>{
            setBgColor(enmConnectCorlor.connecting);
            setConnectMessage('Connecting...');
            setConnectButton({title:'接続中',enable:false});
            setIsConnection(false);
        }
        //接続状態
        NetWorkManager.onWsOpenConnectEx = () =>{
            setBgColor(enmConnectCorlor.connect);
            setConnectMessage('Connect Open.');
            setConnectButton({title:'切断',enable:true});
            setIsConnection(true);
        }
        //切断状態
        NetWorkManager.onWsCloseConnectEx = () =>{
            setBgColor(enmConnectCorlor.disconnect);
            setConnectMessage('Connect Close.');
            setConnectButton({title:'接続',enable:true});
            setIsConnection(false);
        }

    }

    return (
        <Grid container sx={GridSx}>

            <Grid item xs sx={{...GridSx}}></Grid>
            <Grid container sx={{...GridSx, width:"373px"}} >
                <Grid item sx={{...GridSx, width:"100%" , mb:1}} >
                    <Grid item sx={{...GridSx,height:"100%" ,display: 'flex', alignItems: 'center'}}></Grid>
                </Grid>
                <Grid container sx={{...GridSx, width:"100%"}}>
                    <Grid item sx={GridSx}>
                        <input id="txtWsUri" value={wsUri} onChange={handleChange_txtWsUri} readOnly={!conButton.enable} style={{height:"100%"}}/>
                    </Grid>
                    <Grid item sx={GridSx}>
                        <Button id="btnConnect" onClick={handleOnClick_btnConnection} sx={{...ButtonSx,margin:"0px 2px"}} disabled={!conButton.enable} >{conButton.title}</Button>
                    </Grid>
                    <Grid item id="grdConnectColor" sx={{...GridSx,backgroundColor:bgColor,width:'30px'}}></Grid>
                    <Grid item id="grdConnectMsg" sx={{...GridSx,margin:"0px 3px",height:"100%" ,display: 'flex', alignItems: 'center'}}>{conMessage}</Grid>
                </Grid>
            </Grid>
            <Grid item xs sx={{...GridSx}}></Grid>

            {/*
            <Grid item sx={GridSx}>

                <Grid item xs={12} sx={GridSx}>
                    <Grid container sx={GridSx}>
                        <Grid item sx={GridSx}>
                            <input value={`ws://${ServerIp}:${PortNo}`}/>
                        </Grid>
                        <Grid item sx={GridSx}>
                            <Button sx={ButtonSx}>接続</Button>
                        </Grid>
                        <Grid item sx={GridSx}>
                            <Box>aaaa</Box>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            */}
        </Grid>
  )
}

export default CtrlWebSocket
