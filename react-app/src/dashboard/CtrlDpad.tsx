import React from 'react'
import {Box, Button, Grid, Paper} from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'; //↑
import ArrowForwardIcon from '@mui/icons-material/ArrowForward'; //→
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'; //↓
import ArrowBackIcon from '@mui/icons-material/ArrowBack'; //←
import SubOutPrm from './SubOutPrm';
import * as UtilsCommon from '../utils/UtilsCommon';
import UtilsButton from '../utils/UtilsButton';

function CtrlDpad(props:UtilsCommon.DashboardContentProps) {
  const pram = {
    fontSize:"10px",
    Button_w:"40px",
    Button_h:"40px",
    Param_w:"40px",
    Param_h:"40px",
  };
  
  const PaperSx = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: pram.Button_h,
    width: pram.Button_w,
    padding: '0px',
    borderRadius: 0,
    color: 'rgba(0, 0, 0, 0)',
    backgroundColor: 'rgba(0, 0, 0, 0)',
    border:'none',
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

  return (
          <Grid container spacing={0}>
            <Grid container spacing={0.3} sx={{mb:0.1}}>
              <Grid item>
                <Paper sx={PaperSx}>1</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>2</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>4</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>5</Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3} sx={{mb:0.3}}> 
              <Grid item>
                <Paper sx={PaperSx}>6</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>7</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/* 前進ボタン */}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={UtilsCommon.enmButtonType.move_fw}
                  >
                    <ArrowUpwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>9</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>10</Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3} sx={{mb:0.3}}>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/*ボタン 左*/}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={UtilsCommon.enmButtonType.move_left}
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
                  {/*ボタン 右*/}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={UtilsCommon.enmButtonType.move_right}
                  >
                    <ArrowForwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3} sx={{mb:0.3}}> 
              <Grid item>
                <Paper sx={PaperSx}>16</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>17</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>
                  {/*ボタン 後進*/}
                  <UtilsButton 
                    sx={ButtonSx} 
                    variant="contained"
                    props={props} 
                    ButtonType={UtilsCommon.enmButtonType.move_bk}
                  >
                    <ArrowDownwardIcon />
                  </UtilsButton>
                </Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>19</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>20</Paper>
              </Grid>
            </Grid>
            <Grid container spacing={0.3}>
              <Grid item>
                <Paper sx={PaperSx}>21</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>22</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}><SubOutPrm sx={{color: "black", height: pram.Param_h, width:pram.Param_w}}/></Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>24</Paper>
              </Grid>
              <Grid item>
                <Paper sx={PaperSx}>25</Paper>
              </Grid>
            </Grid>
          </Grid>
    )
}

export default CtrlDpad
