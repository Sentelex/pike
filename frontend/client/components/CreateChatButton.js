import React, { useState, useEffect } from 'react';
// import './NewChatButton.css'; // Add styles here

export default function CreateChatButton({ isOpen, setIsOpen }) {
	// Add event listener to detect clicks outside
	// useEffect(() => {
	// 	if (isExpanded) {
	// 		document.addEventListener('click', handleClickOutside);
	// 	} else {
	// 		document.removeEventListener('click', handleClickOutside);
	// 	}

	// 	return () => {
	// 		document.removeEventListener('click', handleClickOutside);
	// 	};
	// }, [isExpanded]);

	const handleClick = () => {
		setIsOpen(true);
		console.log('Click! (isOpen)', isOpen);
	};

	return (
		<div
			id='create-chat-button'
			className={isOpen ? 'expanded' : 'collapsed'}
			onClick={handleClick}
		>
			{isOpen ? 'Create New Chat' : 'New\nChat'}
		</div>
	);
}
