import React from 'react'
import {Box, Button, Grid} from '@mui/material';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
import SubOutPrm from './SubOutPrm';

function CtrlAccel(props: { value: any;}) {
  const {value} = props;
  return (
    <div>
      <Grid container spacing={0}>
        <Grid item xs={0}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: '0px' }}>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleUpIcon />} 
              sx={{ 
                fontSize: '0.75rem',
                fontFamily: 'Courier New, monospace',
                borderRadius: 0,
                height:'40px',
                }}>
              アクセル
            </Button>
            <Button 
              variant="outlined" 
              startIcon={<ArrowCircleDownIcon />} 
              sx={{ 
                fontSize: '0.75rem',
                fontFamily: 'Courier New, monospace',
                borderRadius: 0,
                height:'40px',
                }}>
              アクセル
            </Button>
          </Box>
        </Grid>
        <Grid item sx={{backgroundColor:"red", height:'80px'}}>
          <SubOutPrm value={value} sx={{ height: '80px' }}/>
        </Grid>
      </Grid>
    </div>
  )
}

export default CtrlAccel
