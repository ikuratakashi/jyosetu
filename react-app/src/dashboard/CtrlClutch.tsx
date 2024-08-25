
import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
import SubOutPrm from './SubOutPrm';

function CtrlClutch(props: { value: any;}) {
  const {value} = props;
  
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
          <Box sx={{mb:0.2}}>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleUpIcon />} 
              sx={ButtonSx}>
              クラッチ
            </Button>
          </Box>
          <Box>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleDownIcon />} 
              sx={ButtonSx}>
              クラッチ
            </Button>
          </Box>
        </Grid>
        <Grid item sx={{height:pram.Param_h}}>
          <SubOutPrm value={value} sx={{ height: pram.Param_h, width:pram.Param_w}}/>
        </Grid>
      </Grid>
    </div>
  )
}

export default CtrlClutch
