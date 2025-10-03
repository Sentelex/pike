import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

function CopyButton({ text }) {
	const [copied, setCopied] = React.useState(false);
	const onCopy = async () => {
		try {
			await navigator.clipboard.writeText(text);
			setCopied(true);
			setTimeout(() => setCopied(false), 1200);
		} catch (e) {}
	};
	return (
		<button className="code-copy-btn" onClick={onCopy} aria-label="Copy code">
			{copied ? 'Copied' : 'Copy'}
		</button>
	);
}

export default function AgentMessage({ message }) {
	const getMessageText = () => {
		if (typeof message === 'string') return message;
		const c = message?.content;
		if (!c) return message?.text || message?.message || '';
		if (Array.isArray(c)) {
			return c.map((it) => (typeof it === 'string' ? it : it?.text || ''))
				.filter(Boolean)
				.join('\n');
		}
		return typeof c === 'string' ? c : String(c);
	};

	const content = getMessageText();

	const components = {
		pre({ children }) {
			return <div className="md-pre">{children}</div>;
		},
		code({ inline, className, children, ...props }) {
			const match = /language-(\w+)/.exec(className || '');
			const language = match ? match[1] : undefined;
			if (!inline) {
				const codeText = String(children);
				return (
					<div className="code-block">
						<CopyButton text={codeText} />
						<SyntaxHighlighter
							style={oneDark}
							language={language}
							PreTag="div"
							wrapLongLines={true}
							customStyle={{ borderRadius: 8 }}
							{...props}
						>
							{codeText.replace(/\n$/, '')}
						</SyntaxHighlighter>
					</div>
				);
			}
			return (
				<code className={className} {...props}>
					{children}
				</code>
			);
		},
	};

	return (
		<div className='agent-message'>
			<ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
				{content}
			</ReactMarkdown>
		</div>
	);
}
