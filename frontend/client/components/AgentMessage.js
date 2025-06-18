import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';

export default function AgentMessage({ message }) {
	// Extract content from message
	const getMessageContent = () => {
		if (Array.isArray(message.content)) {
			// Handle array content (find text content)
			const textContent = message.content.find(item => item.type === 'text' || typeof item === 'string');
			return textContent?.text || textContent || message.content.join(' ');
		}
		return message.content || '';
	};

	const content = getMessageContent();

	// Custom components for markdown rendering
	const components = {
		code({ node, inline, className, children, ...props }) {
			const match = /language-(\w+)/.exec(className || '');
			const language = match ? match[1] : '';

			return !inline && language ? (
				<SyntaxHighlighter
					style={oneDark}
					language={language}
					PreTag="div"
					customStyle={{
						margin: '1em 0',
						borderRadius: '8px',
						fontSize: '14px'
					}}
					{...props}
				>
					{String(children).replace(/\n$/, '')}
				</SyntaxHighlighter>
			) : (
				<code
					className={`inline-code ${className || ''}`}
					{...props}
				>
					{children}
				</code>
			);
		},
		pre({ children }) {
			return <div className="code-block-wrapper">{children}</div>;
		},
		p({ children }) {
			return <p className="markdown-paragraph">{children}</p>;
		},
		ul({ children }) {
			return <ul className="markdown-list">{children}</ul>;
		},
		ol({ children }) {
			return <ol className="markdown-ordered-list">{children}</ol>;
		},
		li({ children }) {
			return <li className="markdown-list-item">{children}</li>;
		},
		blockquote({ children }) {
			return <blockquote className="markdown-blockquote">{children}</blockquote>;
		},
		h1({ children }) {
			return <h1 className="markdown-h1">{children}</h1>;
		},
		h2({ children }) {
			return <h2 className="markdown-h2">{children}</h2>;
		},
		h3({ children }) {
			return <h3 className="markdown-h3">{children}</h3>;
		},
		h4({ children }) {
			return <h4 className="markdown-h4">{children}</h4>;
		},
		h5({ children }) {
			return <h5 className="markdown-h5">{children}</h5>;
		},
		h6({ children }) {
			return <h6 className="markdown-h6">{children}</h6>;
		}
	};

	return (
		<div className='agent-message'>
			<ReactMarkdown
				remarkPlugins={[remarkGfm]}
				components={components}
			>
				{content}
			</ReactMarkdown>
		</div>
	);
}
