import React from 'react'
import MarkdownViewer from './CtrlMarkdownViewer'

function Home() {

  const markdownUrl = process.env.PUBLIC_URL + '/doc/ラズパイサーバの使い方.md';

  return (
    <MarkdownViewer url={markdownUrl}/>
  )
}

export default Home
