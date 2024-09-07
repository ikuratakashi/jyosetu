import React, { useRef, useState, useEffect  } from 'react'
import {Box, Button, Grid} from '@mui/material';
import { Select, MenuItem } from '@mui/material';
import * as UtilsCommon from '../utils/UtilsCommon'
import * as UtilsMomoManager from '../utils/UtilsMomoManager';

function CtrlMomoVideo(props: UtilsCommon.DashboardContentProps) {

    const{momomanager} = props;
    const MomoManager = momomanager;

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
        border:'0px solid black',
        marginTop: '1px', // 上にスペースを追加
        marginBottom: '1px' // 下にスペースを追加
    }

    const SelectServerSx = {
        height : '30px',
        width : '230px',
    }
    const SelectCodecsSx = {
        height : '30px',
        width : '90px',
    }

    const VideoSx = {
        maxWidth:'300px'
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
    const [conIsConnection,setIsConnection] = useState(false);
    const [conServerSelectIsReadOnly,setServerSelectIsReadOnly] = useState(false);
    const [conServerSelectValue,setServerSelectValue] = useState('none');
    const [conCodecsSelectValue,setCodecsSelectValue] = useState('H264');
    const [conVideo,setVideoValue] = useState<UtilsMomoManager.MomoVideo | undefined>(undefined);

    //各オブジェクトを操作するときの変数を定義
    //※各コントロールのrefに設定することで変数を経由して操作できる
    const VideoRef = useRef(null);
    const CodecsRef = useRef(null);
    const ServerRef = useRef(null);

    //接続ボタンのクリック時の処理
    const handleOnClick_btnConnection = (event:any) =>{
        if(conIsConnection == true){

            //接続時 → 切断へ

            if(conVideo){
                conVideo?.disconnect();
                MomoManager?.removeVideItem(conVideo);
                setVideoValue(undefined);
            }

            setIsConnection(false);
            setBgColor(UtilsCommon.enmConnectCorlor.disconnect);
            setConnectButton({title:"接続",enable:true})
            setServerSelectIsReadOnly(false);

        }else{
            //切断時 → 接続へ

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
                    VideoElement : VideoRef,
                    MomoServerData : MomoServerValue
                }
            }

            let VideoItem : UtilsMomoManager.MomoVideo | undefined = undefined;
            if(MomoVideoPropsValue){
                if(!conVideo){
                    VideoItem = MomoManager?.addVideoItem(MomoVideoPropsValue);
                    setVideoValue(VideoItem);
                }
                if(conVideo){
                    conVideo?.connect();
                }else{
                    VideoItem?.connect();
                }
            }

            setIsConnection(true); //接続へ
            setBgColor(UtilsCommon.enmConnectCorlor.connect);
            setConnectButton({title:"切断",enable:true})
            setServerSelectIsReadOnly(true);
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
            {/* リストやボタンなど */}
            <Grid container sx={{...GridSx, width:"100%"}}>
                <Grid item sx={GridSx}>
                    <Select 
                        ref={CodecsRef} 
                        defaultValue="H264" 
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
                    <Button id="btnConnect" onClick={handleOnClick_btnConnection} sx={{...ButtonSx,margin:"0px 2px"}} disabled={!conButton.enable} >{conButton.title}</Button>
                </Grid>
                <Grid item id="grdConnectColor" sx={{...GridSx,backgroundColor:bgColor,width:'30px'}}></Grid>
            </Grid>
            {/* カメラ部分*/}
            <Grid container sx={{...GridSx, width:"100%"}}>
                <video ref={VideoRef} style={{width:"100%",maxWidth:"400px"}} controls>
                Your browser does not support the video tag.
                </video>
            </Grid>

        </Grid>
    )
}

export default CtrlMomoVideo
