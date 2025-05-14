import React from 'react';

export default function SendButton({ onClick, disabled = false }) {
	return (
		<button
			className='send-button'
			onClick={onClick}
			disabled={disabled}
			style={{
				backgroundColor: disabled ? '#ccc' : '#007bff',
				color: 'white',
				border: 'none',
				borderRadius: '5px',
				padding: '10px 20px',
				cursor: disabled ? 'not-allowed' : 'pointer',
				fontSize: '16px',
			}}
		>
			Send
		</button>
	);
}
