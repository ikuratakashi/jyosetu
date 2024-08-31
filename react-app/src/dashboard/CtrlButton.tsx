import React from 'react'
import {Box, Button, Grid, Paper} from '@mui/material';
import SubOutPrm from './SubOutPrm';
import * as UtilsCommon from '../utils/UtilsCommon';
import UtilsButton from '../utils/UtilsButton';

//ボタン
///三角
import ChangeHistoryIcon from '@mui/icons-material/ChangeHistory';
///丸
import TripOriginIcon from '@mui/icons-material/TripOrigin';
//バツ
import CloseIcon from '@mui/icons-material/Close';
//四角
import CropSquareIcon from '@mui/icons-material/CropSquare';

function CtrlButton(props: { value: any;} & UtilsCommon.DashboardContentProps) {

    const {value} = props;

    const pram = {
      fontSize:"0.75rem",

      Button_h:"40px",
      Button_w:"70px",

      Paper_h:"40px",
      Paper_w:"30px",

      Param_h:"40px",
      Param_w:"70px",

      BtnCol_Sankaku:"#00CC00",
      BtnCol_Maru:"#EE3333",
      BtnCol_Batu:"#0066CC",
      BtnCol_Shikaku:"#CC66CC",

    };

    const PaperSx = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: pram.Paper_h,
        width: pram.Paper_w,
        padding: '0px',
        borderRadius: 0,
        color: 'rgba(0, 0, 0, 0)',
        backgroundColor: 'rgba(0, 0, 0, 0)',
        border:'none',
        boxShadow: 'none',
    };

    const PaperSxButton = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: pram.Button_h,
        width: pram.Button_w,
        padding: '0px',
        borderRadius: 0,
        color: 'rgba(0, 0, 0, 0)',
        backgroundColor: 'rgba(0, 0, 0, 0)',
//        border:'none',
//        boxShadow: 'none',
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
        border:'none',
        boxShadow: '2px 2px 5px gray',
        backgroundColor:'gray',
        '&:hover': {
            backgroundColor: 'gray',
            filter: 'brightness(0.8)',
            border:'none',
          },
        color:'white',
    };

    const SubOutPrmSx = {
        height: pram.Param_h, 
        width:pram.Param_w,
    };
      
  return (
        <Grid container spacing={0}>

            {/* 1列目 */}
            <Grid container spacing={0} sx={{mb:0.1}}>
                <Grid item>
                    <Paper sx={PaperSx}>1</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>2</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>3</Paper>
                </Grid>
                <Grid item>
                    {/* 数値 */}
                    <Paper sx={PaperSx}><SubOutPrm value={value} sx={SubOutPrmSx}/></Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>5</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>6</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>7</Paper>
                </Grid>
            </Grid>

            {/* 2列目 */}
            <Grid container spacing={0} sx={{mb:0.4}}>
                <Grid item>
                    <Paper sx={PaperSx}>1</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>2</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>3</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>
                        {/*ボタン 三角*/}
                        <Box>
                            <UtilsButton 
                                variant="outlined" 
                                startIcon={<ChangeHistoryIcon sx={{ color: pram.BtnCol_Sankaku }}/>} 
                                sx={ButtonSx}
                                props={props} 
                                ButtonType={UtilsCommon.enmButtonType.btn_sankaku}
                            >
                            ---
                            </UtilsButton>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>5</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>6</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>7</Paper>
                </Grid>
            </Grid>
            
            {/* 3列目 */}
            <Grid container spacing={0} sx={{mb:0.3}}>
                <Grid item>
                    <Paper sx={PaperSx}>1</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>
                        {/*ボタン 四角*/}
                        <Box>
                            <UtilsButton 
                            variant="outlined" 
                            startIcon={<CropSquareIcon sx={{ color: pram.BtnCol_Shikaku }}/>} 
                            sx={ButtonSx}
                            props={props} 
                            ButtonType={UtilsCommon.enmButtonType.btn_sikaku}
                            >
                            ---
                            </UtilsButton>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>3</Paper>
                </Grid>
                <Grid>
                    <Paper sx={PaperSx}>4</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>5</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>
                        {/*ボタン 丸*/}
                        <Box>
                            <UtilsButton 
                            variant="outlined" 
                            startIcon={<TripOriginIcon sx={{ color: pram.BtnCol_Maru }}/>} 
                            sx={ButtonSx}
                            props={props} 
                            ButtonType={UtilsCommon.enmButtonType.btn_on}
                            >
                            回転
                            </UtilsButton>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>7</Paper>
                </Grid>
            </Grid>

            {/* 4列目 */}
            <Grid container spacing={0} sx={{mb:0.2}}>
                <Grid item>
                    <Paper sx={PaperSx}>1</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>2</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>3</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>
                        {/*ボタン バツ*/}
                        <Box>
                            <UtilsButton 
                            variant="outlined" 
                            startIcon={<CloseIcon sx={{ color: pram.BtnCol_Batu }}/>} 
                            sx={ButtonSx}
                            props={props} 
                            ButtonType={UtilsCommon.enmButtonType.btn_off}
                            >
                            停止
                            </UtilsButton>
                        </Box>
                    </Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>5</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>6</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>7</Paper>
                </Grid>
            </Grid>

            {/* 5列目 */}
            <Grid container spacing={0}>
                <Grid item>
                    <Paper sx={PaperSx}>1</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>2</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>3</Paper>
                </Grid>
                <Grid item>
                    {/* 数値 */}
                    <Paper sx={PaperSx}><SubOutPrm value={value} sx={SubOutPrmSx}/></Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>5</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>6</Paper>
                </Grid>
                <Grid item>
                    <Paper sx={PaperSx}>7</Paper>
                </Grid>
            </Grid>

        </Grid>

    )
}

export default CtrlButton
