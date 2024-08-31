import React from 'react'
import {Box, Button, Grid, Paper} from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'; //↑
import ArrowOutwardIcon from '@mui/icons-material/ArrowOutward'; //↗
import ArrowForwardIcon from '@mui/icons-material/ArrowForward'; //→
import SouthEastIcon from '@mui/icons-material/SouthEast'; //↘
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'; //↓
import SouthWestIcon from '@mui/icons-material/SouthWest';//↙
import ArrowBackIcon from '@mui/icons-material/ArrowBack'; //←
import NorthWestIcon from '@mui/icons-material/NorthWest'; //↖
import SyncAltIcon from '@mui/icons-material/SyncAlt';
import SubOutPrm from './SubOutPrm';
import { styled } from '@mui/material/styles';
import * as UtilsCommon from '../utils/UtilsCommon';
import UtilsButton from '../utils/UtilsButton';

function CtrlDpad8(
  props:
  {
    valueUp: any,
    valueUpRithg: any,
    valueRight: any,
    valueRightDown: any,
    valueDown: any,
    valueLeftDown: any,
    valueLeft: any,
    valueLeftUp: any,
    valueLeftRight: any,
    valueUpDown: any,
    AnalogSticType : UtilsCommon.enmAnalogSticType,
  }
  & UtilsCommon.DashboardContentProps
  )
{

  const {
    valueUp,
    valueUpRithg,
    valueRight,
    valueRightDown,
    valueDown,
    valueLeftDown,
    valueLeft,
    valueLeftUp,
    valueLeftRight,
    valueUpDown,
    AnalogSticType,
  } = props;

  //パラメタ出力部分のサイズなど
  const pram = {
    //フォントサイズ
    fontSize:"10px",
    //ボタン部分
    Button_w:"40px",
    Button_h:"40px",
    //8方向キー部分
    Param_w:"40px",
    Param_h:"40px",
    //雪射出口
    ParamOut_w:"80px",
    ParamOut_h:"40px",
  };
  
  const PaperSx = {
    display: 'flex',
    justifyContent: 'center', //水平
    alignItems: 'center', //垂直
    height: pram.Button_h,
    width: pram.Button_w,
    padding: '0px',
    borderRadius: 0,
    backgroundColor: 'rgba(0, 0, 0, 0)',
    color: 'rgba(0, 0, 0, 0)',
//    border:'none',
    boxShadow: 'none',
  };

  const PaperOutSx = {
    display: 'flex',
    justifyContent: 'left', //水平
    alignItems: 'center', //垂直
    height: pram.Button_h,
    width: pram.Button_w,
    padding: '0px',
    borderRadius: 0,
    backgroundColor: 'rgba(0, 0, 0, 0)',
//    color: 'rgba(0, 0, 0, 0)',
//    border:'none',
    boxShadow: 'none',
  };

  const ButtonSx = {
    fontSize: pram.fontSize,
    fontFamily: 'Courier New, monospace',
    borderRadius: 0,
    height: pram.Button_h,
    width: pram.Button_w,
    textAlign: 'center',
    padding: '0px',
    minWidth: '0px',
    backgroundColor:'gray',
    '&:hover': {
      backgroundColor: 'gray',
      filter: 'brightness(0.8)',
      border:'none',
    },
  };

  const SyncAltIcon90 = styled(SyncAltIcon)({
    transform: 'rotate(90deg)'
  });

  return (
          <Grid container spacing={0}>
            <Grid container spacing={0.3} sx={{mb:0.1}}>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueLeftUp} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>2</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueUp} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>4</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueUpRithg} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3} sx={{mb:0.3}}> 
              <Grid item>
                <Paper sx={PaperSx}>6</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 左上 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                        UtilsCommon.enmButtonType.chute_L_lup : 
                        UtilsCommon.enmButtonType.chute_R_lup
                    }
                  >
                    <NorthWestIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 上 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_up :
                      UtilsCommon.enmButtonType.chute_R_up
                    }
                  >
                    <ArrowUpwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 右上 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_rup :
                      UtilsCommon.enmButtonType.chute_R_rup
                    }
                  >
                    <ArrowOutwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>10</Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3} sx={{mb:0.3}}>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueLeft} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 左 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_left :
                      UtilsCommon.enmButtonType.chute_R_left
                    }
                  >
                    <ArrowBackIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>13</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 右 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_right :
                      UtilsCommon.enmButtonType.chute_R_right
                    }
                  >
                    <ArrowForwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueRight} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
            </Grid>

            <Grid container spacing={0.3} sx={{mb:0.3}}> 
              <Grid item>
                <Paper sx={PaperSx}>16</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 左下 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_ldw :
                      UtilsCommon.enmButtonType.chute_R_ldw
                    }
                  >
                    <SouthWestIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                {/* 8方向 下 */}
                <Paper sx={PaperSx}>
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_dw :
                      UtilsCommon.enmButtonType.chute_R_dw
                    }
                  >
                    <ArrowDownwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 8方向 右下 */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={
                      AnalogSticType == UtilsCommon.enmAnalogSticType.left ? 
                      UtilsCommon.enmButtonType.chute_L_rdw :
                      UtilsCommon.enmButtonType.chute_R_rdw
                    }
                  >
                    <SouthEastIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>20</Paper>
              </Grid>
            </Grid>

            <Grid container spacing={0.3} sx={{mb:1.0}}> 
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueLeftDown} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>22</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueDown} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>24</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm value={valueRightDown} sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
            </Grid>

            <Grid container spacing={0.3} sx={{mb:0.1}}> 
              <Grid item>
                <Paper sx={PaperSx}></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperOutSx}><SyncAltIcon /></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperOutSx}><SubOutPrm value={valueLeftRight} sx={{color: "black", height: pram.ParamOut_h, width:pram.ParamOut_w}}/></Paper>
              </Grid>
            </Grid>

            <Grid container spacing={0.3}> 
              <Grid item>
                <Paper sx={PaperSx}></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperOutSx}><SyncAltIcon90 /></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperOutSx}><SubOutPrm value={valueUpDown} sx={{color: "black", height: pram.ParamOut_h, width:pram.ParamOut_w}}/></Paper>
              </Grid>
            </Grid>

          </Grid>
  )
}

export default CtrlDpad8
