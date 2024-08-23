import React from 'react'
import { SidebarData } from './SidebarData'
import SideberIcon from "./SideberIcon.js"

function Sideber() {
  return (
    <div className='Sidebar'>
        <SideberIcon />
        <ul className='SidebarList'>
            {SidebarData.map((value, key) => {
                let isActive = "";
                if(window.location.pathname === value.link || (window.location.pathname === "/" && value.link === "/home")){
                    isActive = "active";
                }else{
                    isActive = "";
                }                
                return (
                    <li 
                        key={key}
                        id={isActive}
                        className='row' 
                        onClick={() => {
                            window.location.pathname = value.link;
                        }}
                    >
                        <div id="icon">{value.icon}</div>
                        <div id="title">{value.title}</div>
                    </li>
                )
            })}
        </ul>
    </div>
  )
}

export default Sideber
