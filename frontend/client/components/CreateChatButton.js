import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import SendButton from './SendButton'; // Import the SendButton component

export default function CreateChatButton({
	isOpen,
	setIsOpen,
	agentId,
	newMessage,
	setNewMessage,
}) {
	const storedChatMessage = useSelector((state) => state.newChatMessage);
	const agents = useSelector((state) => state.agents);
	const dispatch = useDispatch();

	const handleChange = (e) => {
		const { name, value } = e.target;
		setNewMessage(value);
	};

	const handleButtonClick = () => {
		if (!isOpen) {
			setNewMessage(storedChatMessage);
			setIsOpen(true);
			console.log('Click! (isOpen)', isOpen);
		}
	};

	const returnAgentName = (agentId) => {
		const agent = agents.find((agent) => agent.agentId === agentId);
		return agent ? agent.agentName : '';
	};

	const handleSendClick = () => {
		if (newMessage.trim()) {
			setIsOpen(false);
			dispatch({
				type: 'UPDATE_NEW_CHAT_MESSAGE',
				payload: '',
			});
			console.log('Send message:', newMessage);
			setNewMessage(''); // Clear the input
		}
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault(); // Prevent default behavior of adding a new line
			handleSendClick(); // Call the send message function
		}
	};

	return (
		<div
			id='create-chat-button'
			className={isOpen ? 'expanded' : 'collapsed'}
			onClick={handleButtonClick}
		>
			{isOpen ? (
				<>
					<textarea
						name='createChatPrompt'
						inputMode='text'
						autoComplete='off'
						placeholder={`Start a new chat with ${returnAgentName(agentId)}`}
						className='create-chat-input'
						value={newMessage}
						onChange={handleChange}
						onKeyDown={handleKeyDown} // Add keydown listener
						rows={1} // Number of visible text lines
						// cols={30} // Width of the textarea
					/>
					<SendButton
						onClick={handleSendClick}
						disabled={!newMessage.trim()} // Disable if no message
					/>
				</>
			) : (
				'New\nChat'
			)}
		</div>
	);
}
