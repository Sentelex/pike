import React, { useState, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import SendButton from './SendButton';
import { IoAdd } from 'react-icons/io5';
import { RiChatNewLine } from 'react-icons/ri';
import { BiMessageSquareAdd } from 'react-icons/bi';
import { TbMessagePlus } from 'react-icons/tb';
import { createNewChat } from '../store';
import PopupBlanket from './PopupBlanket';

export default function CreateChatButton({
	// isOpen,
	// setIsOpen,
	agentId,
	// newMessage,
	// setNewMessage,
	handleScrollToBottom,
}) {
	const [isOpen, setIsOpen] = useState(false);
	const [newMessage, setNewMessage] = useState('');
	const storedChatMessage = useSelector((state) => state.newChatMessage);
	const agents = useSelector((state) => state.agents);
	const dispatch = useDispatch();

	const [isFullyExpanded, setIsFullyExpanded] = useState(false);
	const textareaRef = useRef(null); // Create a ref for the textarea

	// Adjust the textarea height as the user types
	const adjustTextareaHeight = () => {
		const textarea = textareaRef.current;
		if (textarea) {
			textarea.style.height = 'auto';
			const lineHeight = parseInt(
				window.getComputedStyle(textarea).lineHeight,
				10
			);
			const maxHeight = lineHeight * 5; // limit to 5 lines
			textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px';
			textarea.style.overflowY =
				textarea.scrollHeight > maxHeight ? 'auto' : 'hidden';
		}
	};

	// Trigger a delay to show elements only after expansion is triggered
	useEffect(() => {
		let timeout;
		if (isOpen) {
			timeout = setTimeout(() => {
				setIsFullyExpanded(true);
				requestAnimationFrame(() => {
					textareaRef.current?.focus();
					adjustTextareaHeight();
				});
			}, 20); // Adjust delay here
		} else {
			setIsFullyExpanded(false);
		}
		return () => clearTimeout(timeout);
	}, [isOpen]);

	const handleChange = (e) => {
		const { value } = e.target;
		setNewMessage(value);
		adjustTextareaHeight();
	};

	const handleButtonClick = () => {
		if (!isOpen) {
			setNewMessage(storedChatMessage);
			setIsOpen(true);
			adjustTextareaHeight();
		}
	};

	const returnAgentName = (agentId) => {
		const agent = agents.find((agent) => agent.agentId === agentId);
		return agent ? agent.agentName : '';
	};

	const handleSendClick = () => {
		if (newMessage.trim()) {
			setIsOpen(false);
			dispatch(createNewChat(1, agentId, newMessage)).then(() => {
				if (handleScrollToBottom) {
					handleScrollToBottom();
				}
			});
			setNewMessage('');
		}
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault(); // Prevent default behavior of adding a new line
			handleSendClick(); // Call the send message function
		}
	};

	return (
		<>
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
							className={`create-chat-input ${
								isFullyExpanded ? 'fade-in' : ''
							}`}
							value={isFullyExpanded ? newMessage : ''}
							onChange={handleChange}
							onKeyDown={handleKeyDown}
							rows={1}
						/>
						<div
							style={{
								minHeight: '100%',
								display: 'flex',
								alignSelf: 'flex-end',
							}}
						>
							<SendButton
								onClick={handleSendClick}
								disabled={!newMessage.trim()} // Disable if no message
								isFullyExpanded={isFullyExpanded}
							/>
						</div>
					</>
				) : (
					<div
						style={{
							display: 'flex',
							alignItems: 'center',
							paddingRight: '10px',
							gap: '5px',
						}}
					>
						<div className={'button-icon-wrapper'}>
							<TbMessagePlus style={{ transform: 'scaleX(-1)' }} />
						</div>
						New Chat
					</div>
				)}
			</div>
			<PopupBlanket
				isOpen={isOpen}
				setIsOpen={setIsOpen}
				newMessage={newMessage}
			/>
		</>
	);
}
