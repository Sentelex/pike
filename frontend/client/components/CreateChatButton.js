import React, { useState, useEffect, useRef } from 'react';

export default function CreateChatButton({ isOpen, setIsOpen }) {
	const [newMessage, setNewMessage] = useState('');
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

	// const handleInput = (e) => {
	// 	setNewMessage(e.target.innerText);
	// 	e.target.style.height = 'auto'; // Reset height
	// 	e.target.style.height = `${e.target.scrollHeight}px`; // Adjust height
	// };

	const inputRef = useRef(null);
	let typingTimeout = useRef(null);

	const handleDebouncedInput = () => {
		// Clear the previous timeout
		clearTimeout(typingTimeout.current);

		// Set a new timeout to update the state after typing stops
		typingTimeout.current = setTimeout(() => {
			if (inputRef.current) {
				setNewMessage(inputRef.current.innerText);
				console.log('Message saved:', inputRef.current.innerText);
			}
		}, 500); // Adjust debounce delay as needed
	};

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
			{isOpen ? (
				<div
					id='new-message-input'
					className='input-field'
					contentEditable='true'
					ref={inputRef}
					onInput={handleDebouncedInput}
					placeholder='Type your message here...'
					style={{
						overflow: 'hidden',
						resize: 'none',
						minHeight: '50px',
						width: '100%',
					}}
				>
					{newMessage}
				</div>
			) : (
				'New\nChat'
			)}
		</div>
	);
}
