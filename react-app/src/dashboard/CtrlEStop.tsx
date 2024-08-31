import React from 'react'
import {Button, Grid} from '@mui/material';
import './CtrlEStop.css';
import SubOutPrm from './SubOutPrm';
import * as UtilsCommon from '../utils/UtilsCommon';
import UtilsButton from '../utils/UtilsButton';

function CtrlEStop(props: { value: any} & UtilsCommon.DashboardContentProps) {

    const {value} = props;

    const pram = {
        Param_h:"40px",
        Param_w:"200px",
    };
    
    //ボタンの種類
    const ButtonType : UtilsCommon.enmButtonType = UtilsCommon.enmButtonType.btn_em;

    return (
    <Grid container spacing={0}>
        <Grid container spacing={0.3} sx={{mb:0.3}}>
            <Grid item xs={0}>
                <UtilsButton sx={{padding:0}} props={props} ButtonType={ButtonType}>
                    <div className="emergency-stop-button"><span>STOP</span></div>
                </UtilsButton>
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
