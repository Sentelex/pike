import React, { useState, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import SendButton from './SendButton';
import { IoAdd } from 'react-icons/io5';

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

	const [isFullyExpanded, setIsFullyExpanded] = useState(false);
	const textareaRef = useRef(null); // Create a ref for the textarea

	// Trigger a delay to show the placeholder after expansion
	useEffect(() => {
		let timeout;
		if (isOpen) {
			timeout = setTimeout(() => {
				setIsFullyExpanded(true);
				textareaRef.current?.focus(); // Focus the textarea when expanded
			}, 25); // Adjust delay to match CSS transition
		} else {
			setIsFullyExpanded(false);
		}
		return () => clearTimeout(timeout);
	}, [isOpen]);

	const handleChange = (e) => {
		const { value } = e.target;
		setNewMessage(value);
	};

	const handleButtonClick = () => {
		if (!isOpen) {
			setNewMessage(storedChatMessage);
			setIsOpen(true);
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
						ref={textareaRef} // Attach the ref to the textarea
						name='createChatPrompt'
						inputMode='text'
						autoComplete='off'
						placeholder={
							isFullyExpanded
								? `Start a new chat with ${returnAgentName(agentId)}`
								: ''
						}
						className={`create-chat-input ${isFullyExpanded ? 'fade-in' : ''}`}
						value={isFullyExpanded ? newMessage : ''}
						onChange={handleChange}
						onKeyDown={handleKeyDown}
						rows={1}
					/>
					<SendButton
						onClick={handleSendClick}
						disabled={!newMessage.trim()} // Disable if no message
						isFullyExpanded={isFullyExpanded}
					/>
				</>
			) : (
				<div
					style={{
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						paddingRight: '10px',
					}}
				>
					<div id={'plus-sign-wrapper'}>
						<IoAdd />{' '}
					</div>{' '}
					New Chat
				</div>
			)}
		</div>
	);
}
