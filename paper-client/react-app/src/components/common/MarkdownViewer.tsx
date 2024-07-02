import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownDisplayProps {
    markdownText: string;
}

const MarkdownDisplay: React.FC<MarkdownDisplayProps> = ({ markdownText }) => {
    return (
        <div className="markdown-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdownText}</ReactMarkdown>
        </div>
    );
};

export default MarkdownDisplay;
