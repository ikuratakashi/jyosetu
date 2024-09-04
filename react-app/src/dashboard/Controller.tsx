/* 
  コントローラー画面
*/
import React from 'react';
import { Box, Grid, Paper } from '@mui/material';
import CtrlClutch from './CtrlClutch';
import CtrlAccel from './CtrlAccel';
import CtrlDpad from './CtrlDpad';
import CtrlButton from './CtrlButton';
import CtrlEStop from './CtrlEStop';
import CtrlDpad8 from './CtrlDpad8';
import * as UtilsCommon from '../utils/UtilsCommon';
import GameComponent from './CtrlGamePad';
import CtrlWebSocket from './CtrlWebSocket';

function Controller(props: UtilsCommon.DashboardContentProps) {
  
  return (
    <Grid container spacing={1} sx={{ height: '100%' }}>
      <Grid item style={{ width: '550px', height: '100%' }}>
        <Paper sx={{ backgroundColor: 'lightblue', height: '100%' }}>
          {/* ラズパイのサーバー接続 */}
          <Grid container sx={{width:'100%',mb:1}}>
            <CtrlWebSocket {...props}></CtrlWebSocket>
          </Grid>
          {/* クラッチとアクセル */}
          <Grid container sx={{width: '100%',mb:1}}>
            <Grid item xs></Grid>
            <Grid item sx={{width:'150px'}}>
              {/* クラッチ */}
              <CtrlClutch {...props}/>
            </Grid>
            <Grid item sx={{width:'70px'}}></Grid>
            <Grid item sx={{width:'150px'}}>
              {/* アクセル */}
              <CtrlAccel {...props}/>
            </Grid>
            <Grid item xs></Grid>
          </Grid>

          {/* 十字キーとボタン */}
          <Grid container 
            sx={{
                  width: '100%',
                  //border:"1px black solid",
                  mb:1,
                }}
          >
            <Grid item xs></Grid>
            <Grid item 
                  sx={{
                        height:'100%',width:"220px",
                        //border:"1px solid black",
                        display:'flex',
                        alignItems: 'center', // 垂直方向の中央揃え
                        justifyContent: 'center' // 水平方向の中央揃え
                      }}
            >
              {/* 十字キー */}
              <CtrlDpad {...props}/>
            </Grid>
            <Grid item sx={{width:'30px'}}></Grid>
            <Grid item 
                  sx={{
                        height:'100%',width:"215px",
                        //border:"1px solid black",
                        display:'flex',
                        alignItems: 'center', // 垂直方向の中央揃え
                        justifyContent: 'center' // 水平方向の中央揃え
                      }}
            >
              {/* ボタン */}
              <CtrlButton {...props}/>
            </Grid>
            <Grid item xs></Grid>
          </Grid>

          {/* 緊急停止ボタン */}
          <Grid container sx={{width: '100%',mb:1}}>
            <Grid item xs></Grid>
            <Grid item 
                  sx={{
                        //border:"solid black 1px",
                        width:'205px',
                        display:'flex',
                        alignItems: 'center', // 垂直方向の中央揃え
                        justifyContent: 'center' // 水平方向の中央揃え
                      }}>
              {/* 緊急停止ボタン */}
              <CtrlEStop {...props}/>
            </Grid>
            <Grid item xs></Grid>
          </Grid>

          {/* 雪射出口の操作 */}
          <Grid container 
            sx={{
                  width: '100%',
                  //border:"1px black solid",
                  mb:1,
                }}
          >
            <Grid item xs></Grid>
            <Grid item 
                  sx={{
                        height:'100%',width:"220px",
                        //border:"1px solid black",
                        display:'flex',
                        alignItems: 'center', // 垂直方向の中央揃え
                        justifyContent: 'center' // 水平方向の中央揃え
                      }}
            >

              {/* 8方向キー */}
              <CtrlDpad8 
                {...props}
                analogstictype={UtilsCommon.enmAnalogSticType.left}
              />
            </Grid>
            <Grid item sx={{width:'30px'}}></Grid>
            <Grid item 
                  sx={{
                        height:'100%',width:"215px",
                        //border:"1px solid black",
                        display:'flex',
                        alignItems: 'center', // 垂直方向の中央揃え
                        justifyContent: 'center' // 水平方向の中央揃え
                      }}
            >
              {/* 8方向キー */}
              <CtrlDpad8 
                {...props}
                analogstictype={UtilsCommon.enmAnalogSticType.right}
              />
            </Grid>
            <Grid item xs></Grid>
          </Grid>

        </Paper>
      </Grid>
      <Grid item style={{ width: '300px', height: '100%' }}>
        <Paper sx={{ backgroundColor: 'lightgreen', height: '100%' }}>
          2列目: 200px
          <GameComponent />
        </Paper>
      </Grid>
      <Grid item xs sx={{ height: '100%' }}>
        <Paper sx={{ backgroundColor: 'lightcoral', height: '100%' }}>
          3列目: 残り
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Controller;
