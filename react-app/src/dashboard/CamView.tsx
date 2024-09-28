import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import { DashboardContentProps } from '../utils/UtilsCommon';
import CtrlMomoVideo from './CtrlMomoVideo';

function CamView(props: DashboardContentProps) {

    return (
        <div>
            <CtrlMomoVideo {...props}/>
        </div>
    )
}

export default CamView
