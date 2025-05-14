import React, { useState, useEffect } from 'react';

export default function PopupBlanket({ isOpen, setIsOpen }) {
	const handleClick = () => {
		setIsOpen(false);
		console.log('Click! (isOpen)', isOpen);
	};

	return (
		<div
			className='popup-blanket'
			style={{ display: isOpen ? 'block' : 'none' }}
			onClick={handleClick}
		></div>
	);
}
