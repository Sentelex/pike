import React from 'react';

export default function AgentMessage({ message }) {
	return (
		<div className='agent-message'>
			{Array.isArray(message.content) ? message.content.text : message.content}
		</div>
	);
}
