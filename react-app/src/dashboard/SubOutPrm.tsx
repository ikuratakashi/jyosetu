import React from 'react'
import { Box } from '@mui/material';
import { CenterFocusWeak } from '@mui/icons-material';

function SubOutPrm(props: { value: any; sx: any; }) {
  const {value,sx} = props;
  return (
    <div>
      <Box
      sx={{
        display: 'flex', // フレックスボックスを使用
        justifyContent: 'right', // 水平方向の中央揃え
        alignItems: 'center', // 垂直方向の中央揃え
        padding: '4px 8px',
        border: '1px solid dimgray',
        fontSize: '1rem', // フォントサイズを調整
        fontFamily: 'Courier New, monospace', // 等幅フォントを使用
        backgroundColor:'white',
        color: "black", 
        ...sx,
      }}
    >
      {value == "" ? "　" : value}
    </Box>
    </div>
  )
}

export default SubOutPrm
