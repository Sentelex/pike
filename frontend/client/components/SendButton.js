import React from 'react';
import { IoArrowUpOutline } from 'react-icons/io5';

export default function SendButton({
	onClick,
	disabled = false,
	isFullyExpanded,
}) {
	return (
		<div
			className={`send-button ${disabled ? 'inactive' : 'active'} ${
				isFullyExpanded ? 'fade-in' : ''
			}`}
			onClick={onClick}
			disabled={disabled}
			// style={{
			// 	color: disabled ? 'gray' : 'black',
			// 	backgroundColor: disabled ? 'lightgrey' : 'white',
			// 	border: disabled ? '1px solid white' : '1px solid gray',
			// 	color: 'white',
			// 	border: 'none',
			// 	borderRadius: '5px',
			// 	padding: '10px 20px',
			// 	cursor: disabled ? 'not-allowed' : 'pointer',
			// 	fontSize: '16px',
			// }}
		>
			<IoArrowUpOutline />
		</div>
	);
}
