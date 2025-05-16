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
		>
			<IoArrowUpOutline />
		</div>
	);
}
