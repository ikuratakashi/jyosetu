import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import VideocamIcon from '@mui/icons-material/Videocam';

import { useNavigate } from 'react-router-dom';

export const mainListItems = (
  <React.Fragment>

    {/* ----------------------------------------

      Home                                     

    -------------------------------------------- */}
    <ListItemButton
        onClick={() => {
          window.location.pathname = "./jyosetu/home";
      }}
    >
      <ListItemIcon>
        {/* アイコンを変えたいときはココを設定 */}
        <HomeIcon />
      </ListItemIcon>
      <ListItemText primary="Home" />
    </ListItemButton>

    {/* ---------------------------------------- 

      Controller                               

    -------------------------------------------- */}
    <ListItemButton
        onClick={() => {
          window.location.pathname = "./jyosetu/controller";
      }}
    >
      <ListItemIcon>
        {/* アイコンを変えたいときはココを設定 */}
        <VideogameAssetIcon /> 
      </ListItemIcon>
      <ListItemText primary="Controller" />
    </ListItemButton>

    {/* ---------------------------------------- 

      カメラ                                   

    -------------------------------------------- */}
    <ListItemButton
        onClick={() => {
          window.location.pathname = "./jyosetu/camview";
      }}
    >
      <ListItemIcon>
        {/* アイコンを変えたいときはココを設定 */}
        <VideocamIcon /> 
      </ListItemIcon>
      <ListItemText primary="Camela" />
    </ListItemButton>

  </React.Fragment>
);

