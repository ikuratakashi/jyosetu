import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import {CtrlWebSocketProps} from '../utils/UtilsNetworkManager'
import { Height } from '@mui/icons-material';
import {enmConnectCorlor} from '../utils/UtilsCommon'

function CtrlWebSocket(props : CtrlWebSocketProps) {
    const{PortNo,ServerIp} = props;

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
    
    return (
        <Grid container sx={GridSx}>

            <Grid item xs sx={{...GridSx}}></Grid>
            <Grid container sx={{...GridSx, width:"390px"}}>
                <Grid item sx={{...GridSx, width:"100%"}}>
                    <Grid item sx={{...GridSx,height:"100%" ,display: 'flex', alignItems: 'center'}}>MainServer Connect</Grid>
                </Grid>
                <Grid container sx={{...GridSx, width:"100%"}}>
                    <Grid item sx={GridSx}>
                        <input value={`ws://${ServerIp}:${PortNo}`} style={{height:"100%"}}/>
                    </Grid>
                    <Grid item sx={GridSx}>
                        <Button sx={{...ButtonSx,margin:"0px 2px"}}>接続</Button>
                    </Grid>
                    <Grid item sx={{...GridSx,backgroundColor:enmConnectCorlor.disconnect,width:'30px'}}></Grid>
                    <Grid item sx={{...GridSx,margin:"0px 3px",height:"100%" ,display: 'flex', alignItems: 'center'}}>Connect None</Grid>
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
