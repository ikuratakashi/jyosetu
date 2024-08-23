
import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
import SubOutPrm from './SubOutPrm';

function CtrlClutch(props: { value: any;}) {
  const {value} = props;
  
  const prameter = {
    fontSize:"0.5rem",
    Buttn_height:"30px",
    Param_height:"60px",
  };

  return (
    <div>
      <Grid container spacing={0}>
        <Grid item xs={0}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleUpIcon />} 
              sx={{ 
                fontSize: prameter.fontSize,
                fontFamily: 'Courier New, monospace',
                borderRadius: 0,
                height:prameter.Buttn_height,
                }}>
              クラッチ
            </Button>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleDownIcon />} 
              sx={{ 
                fontSize: prameter.fontSize,
                fontFamily: 'Courier New, monospace',
                borderRadius: 0,
                height:prameter.Buttn_height,
                }}>
              クラッチ
            </Button>
          </Box>
        </Grid>
        <Grid item sx={{backgroundColor:"red", height:prameter.Param_height}}>
          <SubOutPrm value={value} sx={{ height: prameter.Param_height}}/>
        </Grid>
      </Grid>
    </div>
  )
}

export default CtrlClutch
