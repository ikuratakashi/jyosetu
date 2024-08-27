import React from 'react'
import {Button, Grid} from '@mui/material';
import './CtrlEStop.css';
import SubOutPrm from './SubOutPrm';

interface DashboardContentProps {
    sendMessage: (message: string) => void;
}
function CtrlEStop(props: { value: any} & DashboardContentProps) {

    const {value,sendMessage} = props;

    const pram = {
        Param_h:"40px",
        Param_w:"200px",
        };

    const handleClick = () => {
        sendMessage('Your message here');
    };

    return (
    <Grid container spacing={0}>
        <Grid container spacing={0.3} sx={{mb:0.3}}>
            <Grid item xs={0}>
                <Button sx={{padding:0}} onClick={handleClick}>
                    <div className="emergency-stop-button"><span>STOP</span></div>
                </Button>
            </Grid>
        </Grid>
        <Grid container spacing={0.3}>
            <Grid item sx={{height:pram.Param_h}}>
                <SubOutPrm value={value} sx={{ height: pram.Param_h, width:pram.Param_w}}/>
            </Grid>
        </Grid>
    </Grid>
    )
}

export default CtrlEStop
