import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
import SubOutPrm from './SubOutPrm';
import { DashboardContentProps } from '../utils/UtilsCommon';
import * as UtilsCommon from '../utils/UtilsCommon';
import UtilsButton from '../utils/UtilsButton';

function CtrlAccel(props: { value: any;} & DashboardContentProps) {
    const {value} = props;

    const ButtonTypeUp : UtilsCommon.enmButtonType = UtilsCommon.enmButtonType.accel_up;
    const ButtonTypeDw : UtilsCommon.enmButtonType = UtilsCommon.enmButtonType.accel_dw;

    const pram = {
        fontSize:"0.6rem",
        Button_h:"40px",
        Param_h:"82px",
        Param_w:"50px",
      };
    
      const ButtonSx = { 
        fontSize: pram.fontSize,
        fontFamily: 'Courier New, monospace',
        borderRadius: 0,
        height:pram.Button_h,
        backgroundColor:'gray',
        '&:hover': {
          backgroundColor: 'gray',
          filter: 'brightness(0.8)',
          border:'none',
        },
        color:'white',
        border:'none',
        boxShadow: '2px 2px 5px gray',
      }

      return (
        <div>
          <Grid container spacing={0.3}>
            <Grid item xs={0}>
              <Box sx={{mb:0.3}}>
                <UtilsButton 
                  variant="outlined" 
                  ButtonType={ButtonTypeUp}
                  startIcon={<ArrowCircleUpIcon />} 
                  props={props}
                  sx={ButtonSx}>
                  アクセル
                </UtilsButton>
              </Box>
              <Box>
                <UtilsButton 
                  variant="outlined" 
                  ButtonType={ButtonTypeDw}
                  startIcon={<ArrowCircleDownIcon />} 
                  props={props}
                  sx={ButtonSx}>
                  アクセル
                </UtilsButton>
              </Box>
            </Grid>
            <Grid item sx={{height:pram.Param_h}}>
              <SubOutPrm value={value} sx={{ height: pram.Param_h, width:pram.Param_w}}/>
            </Grid>
          </Grid>
        </div>
      )
}

export default CtrlAccel
