import React from 'react';

export default function UserMessage({ message }) {
	const renderContent = (content, index) => {
		switch (content.type) {
			case 'text':
				return (
					<p key={index} style={{ margin: '0px', marginBottom: '15px' }}>
						{content.text}
					</p>
				);
			case 'image':
				return (
					<img
						key={index}
						src={'/squeaky_bone.jpg'}
						alt={content.alt || 'User sent image'}
					/>
				);
			default:
				return <span key={index}>{JSON.stringify(content)}</span>;
		}
	};

	return (
		<div className='user-message'>
			{Array.isArray(message.content)
				? message.content.map((content, index) => renderContent(content, index))
				: message.content}
		</div>
	);
}
