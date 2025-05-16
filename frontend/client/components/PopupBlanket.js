import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';

export default function PopupBlanket({ isOpen, setIsOpen, newMessage }) {
	const dispatch = useDispatch();
	const handleClick = () => {
		setIsOpen(false);
		dispatch({
			type: 'UPDATE_NEW_CHAT_MESSAGE',
			payload: newMessage,
		});
		console.log('Click! (isOpen) and message:', isOpen, newMessage);
	};

	return (
		<div
			className={`popup-blanket ${isOpen ? 'visible' : ''}`}
			onClick={handleClick}
		></div>
	);
}
