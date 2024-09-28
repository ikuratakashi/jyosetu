import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import 'github-markdown-css/github-markdown.css';
import '../App.css'

interface MarkdownViewerProps {
    url?: string;
}
  
const MarkdownViewer:React.FC<MarkdownViewerProps> = ({url = ""}) => {
  const [markdown, setMarkdown] = useState('');
  const PUBLIC_URL = process.env.PUBLIC_URL;

  useEffect(() => {
    fetch(url)
      .then((response) => response.text())
      .then((text) => {

            const updatedText = text.replace(
                /https:\/\/github\.com\/ikuratakashi\/jyosetu\/raw\/develop-ikura/g, 
                process.env.PUBLIC_URL);

            setMarkdown(updatedText)

        });
  }, [url]);

  return (
    <div className="markdown-container markdown-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {markdown}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;
