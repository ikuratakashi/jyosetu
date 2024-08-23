/* 
  コントローラー画面
*/
import React from 'react';
import { Grid, Paper } from '@mui/material';
import CtrlClutch from './CtrlClutch';
import CtrlAccel from './CtrlAccel';

function Controller() {
  return (
    <Grid container spacing={1} sx={{ height: '100%' }}>
      <Grid item style={{ width: '400px', height: '100%' }}>
        <Paper sx={{ backgroundColor: 'lightblue', height: '100%' }}>

          {/* クラッチ */}
          <CtrlClutch value={"0"}/>
          
          {/* アクセル */}
          <CtrlAccel value={"0"}/>

        </Paper>
      </Grid>
      <Grid item style={{ width: '200px', height: '100%' }}>
        <Paper sx={{ backgroundColor: 'lightgreen', height: '100%' }}>
          2列目: 200px
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
