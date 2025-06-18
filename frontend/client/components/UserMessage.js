import React from 'react';

export default function UserMessage({ message }) {
	const renderContent = (content, index) => {
		switch (content.type) {
			case 'text':
				return (
					<div key={index} className="user-text-content">
						{content.text}
					</div>
				);
			case 'image':
				return (
					<img
						key={index}
						src={'/squeaky_bone.jpg'}
						alt={content.alt || 'User sent image'}
						className="user-image-content"
					/>
				);
			default:
				return <span key={index}>{JSON.stringify(content)}</span>;
		}
	};

	// Handle simple string content with proper line breaks
	const renderSimpleContent = (content) => {
		return (
			<div className="user-text-content">
				{content}
			</div>
		);
	};

	return (
		<div className='user-message'>
			{Array.isArray(message.content)
				? message.content.map((content, index) => renderContent(content, index))
				: renderSimpleContent(message.content)}
		</div>
	);
}
