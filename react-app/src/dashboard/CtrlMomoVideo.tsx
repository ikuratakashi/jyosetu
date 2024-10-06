import React, { useRef, useState, useEffect  } from 'react'
import {Box, Button, Grid} from '@mui/material';
import { Select, MenuItem } from '@mui/material';
import * as UtilsCommon from '../utils/UtilsCommon'
import * as UtilsMomoManager from '../utils/UtilsMomoManager';
import { Margin } from '@mui/icons-material';

/**
 * 接続ステータス
 */
enum ConnectStatus {
    Connect ,
    Connecting ,
    DisConnect
}

function CtrlMomoVideo(props: UtilsCommon.DashboardContentProps) {

    const{momomanager} = props;
    const MomoManager = momomanager;

    const ButtonSx = {
        fontSize: "10px",
        fontFamily: 'Courier New, monospace',
        borderRadius: 0.5,
        height: '25px',
        width: '50px',
        textAlign: 'center',
        minWidth: '0px',
        color:"white",
        backgroundColor:'gray',
        '&:hover': {
          backgroundColor: 'gray',
          filter: 'brightness(0.8)',
          border:'none',
        },
        border:'0px solid black',
        margin:'2px 1px',
    };

    const GridSx ={
        border:'0px solid black',
        marginTop: '0px', // 上にスペースを追加
        marginBottom: '0px' // 下にスペースを追加
    }

    const SelectServerSx = {
        height : '25px',
        width : '165px',
        fontSize : '10px',
        padding: '0px',
        minWidth: '0px',
    }
    const SelectCodecsSx = {
        height : '25px',
        width : '75px',
        fontSize : '10px',
        padding: '0px',
        minWidth: '0px',
    }

    const VideoStyle = {
        width:'100%',
        maxWidth:'414px'
    }

    const ConnectBox = {
        marginTop:'2px',
        height:'25px',
        width:'30px',
    }

    //映像配信サーバmomoのリスト内容
    let MomoServer = [
        { value: 'none', label: '' }
    ];
    const tmpList = MomoManager?.cleateServerSelectList();
    if(tmpList){
        tmpList.forEach((optionValue, index) => {
            if(optionValue){
                MomoServer.push
                (
                    {
                        value : optionValue.value,
                        label : optionValue.label,
                    }
                );
        
            }
        });
    }
    //console.log(`MomoServer = ${JSON.stringify(MomoServer, null, 2)}`);

    //コーデックのリスト内容
    const Codecs = MomoManager?.CodecItems;

    //ステータスの定義
    const [bgColor,setBgColor] = useState(UtilsCommon.enmConnectCorlor.disconnect);
    const [conButton,setConnectButton] = useState({title:'接続',enable:true});
    const [conMessage,setConnectMessage] = useState('Connect None');
    const [conIsConnection,setIsConnection] = useState<ConnectStatus>(ConnectStatus.DisConnect);
    const [conServerSelectIsReadOnly,setServerSelectIsReadOnly] = useState(false);
    const [conServerSelectValue,setServerSelectValue] = useState('none');
    const [conCodecsSelectValue,setCodecsSelectValue] = useState(MomoManager?.CodecDefalut);
    const [conVideo,setVideoValue] = useState<UtilsMomoManager.MomoVideo | undefined>(undefined);

    //各オブジェクトを操作するときの変数を定義
    //※各コントロールのrefに設定することで変数を経由して操作できる
    const VideoRef = useRef<HTMLVideoElement>(null);
    const CodecsRef = useRef(null);
    const ServerRef = useRef(null);

    useEffect(() => {
        const videoElement = VideoRef.current;
    }, []);    

    //接続ボタンのクリック時の処理
    const handleOnClick_btnConnection = (event:any) =>{

        if(conIsConnection == ConnectStatus.Connect || conIsConnection == ConnectStatus.Connecting){
            //接続時 → 切断へ
            //接続中 → 切断へ
            if(conVideo){
                conVideo?.disconnect();
                MomoManager?.removeVideItem(conVideo);
                setVideoValue(undefined);
            }

            setIsConnection(ConnectStatus.DisConnect);
            setBgColor(UtilsCommon.enmConnectCorlor.disconnect);
            setConnectButton({title:"接続",enable:true})
            setServerSelectIsReadOnly(false);

        }else if(conIsConnection == ConnectStatus.DisConnect){
            //切断時 → 接続中 → カメラと接続出来たら → 接続へ
            //　　　   　　　 → カメラと接続出来なかったら → 切断へ

            setIsConnection(ConnectStatus.Connecting); //接続中へ
            setBgColor(UtilsCommon.enmConnectCorlor.connecting);
            setConnectButton({title:"接続中.",enable:true})
            setServerSelectIsReadOnly(true);

            let MomoServerValue : UtilsMomoManager.MomoServer | undefined = undefined;
            if(MomoManager?.ServerItems){
                for (let server of MomoManager?.ServerItems) {
                    if (server.ServerData.DeviceName === conServerSelectValue) {
                        MomoServerValue = server;
                        break;
                    }
                }
            }

            let MomoVideoPropsValue : UtilsMomoManager.MomoVideoProps | undefined = undefined;
            if(MomoServerValue){
                MomoVideoPropsValue = {
                    Codecs : conCodecsSelectValue,
                    VideoElement : VideoRef.current,
                    MomoServerData : MomoServerValue
                }
            }

            let ConnectOK = () =>{
                setIsConnection(ConnectStatus.Connect); //接続へ
                setBgColor(UtilsCommon.enmConnectCorlor.connect);
                setConnectButton({title:"切断",enable:true})
                setServerSelectIsReadOnly(true);
            }

            let ConnectNG = () =>{
                setIsConnection(ConnectStatus.DisConnect); //接続解除へ
                setBgColor(UtilsCommon.enmConnectCorlor.disconnect);
                setConnectButton({title:"接続",enable:true})
                setServerSelectIsReadOnly(false);
            }

            let MomoVideoItem : UtilsMomoManager.MomoVideo | undefined = undefined;
            if(MomoVideoPropsValue){

                if(!conVideo){
                    MomoVideoItem = MomoManager?.addVideoItem(MomoVideoPropsValue);
                    setVideoValue(MomoVideoItem);
                }else{
                    MomoVideoItem = conVideo;
                }

                if(MomoVideoItem){
                    MomoVideoItem.WsOpenEx = () =>{
                        MomoVideoItem?.connect();
                        ConnectOK();
                    }
                    MomoVideoItem.WsErrorEx = () =>{
                        ConnectNG();
                    }

                    //**************************************** */
                    // WebSocketの実行と接続
                    //**************************************** */
                    MomoVideoItem.SetWebSocket();

                }else{
                    ConnectNG();
                }
            }else{
                ConnectNG();
            }
        }
    }

    //コーデックの選択時の処理
    const handleOnSelect_selCodecsList = (event:any)=>{
        setCodecsSelectValue(event.target.value)        
    }

    //サーバリストの選択時の処理
    const handleOnSelect_selServerList = (event:any)=>{
        setServerSelectValue(event.target.value)        
    }

    return (
        <Grid container sx={GridSx}>
            {/***************************
             
              リストやボタンなど 

            *****************************/}
            <Grid container sx={{...GridSx, width:"100%", /*display:"none"*/}}>
                <Grid item sx={GridSx}>
                    <Select 
                        ref={CodecsRef} 
                        defaultValue={MomoManager?.CodecDefalut} 
                        sx={SelectCodecsSx} 
                        readOnly={conServerSelectIsReadOnly}
                        onChange={handleOnSelect_selCodecsList}
                    >
                        {Codecs?.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                            {option.label}
                            </MenuItem>
                        ))}
                    </Select>
                </Grid>
                <Grid item sx={{...GridSx}}>
                    <Select 
                        ref={ServerRef}
                        sx={SelectServerSx} 
                        value={conServerSelectValue}
                        onChange={handleOnSelect_selServerList}
                        readOnly={conServerSelectIsReadOnly}
                    >
                        {MomoServer?.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                            {option.label}
                            </MenuItem>
                        ))}
                    </Select>
                </Grid>
                <Grid item sx={GridSx}>
                    <Button onClick={handleOnClick_btnConnection} sx={ButtonSx} disabled={!conButton.enable} >{conButton.title}</Button>
                </Grid>
                <Grid item sx={{...GridSx,...ConnectBox,backgroundColor:bgColor}}></Grid>
            </Grid>
            {/***************************

              カメラ部分

            *****************************/}
            <Grid container sx={{...GridSx, width:"100%"}}>
                <video ref={VideoRef} style={VideoStyle} controls>
                Your browser does not support the video tag.
                </video>
            </Grid>

        </Grid>
    )
}

export default CtrlMomoVideo
