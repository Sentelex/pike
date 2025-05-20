import React, { useState, useRef } from 'react';
import SendButton from './SendButton';

export default function ChatMessageInput({ onSend, isOpen }) {
	const [message, setMessage] = useState('');
	const textareaRef = useRef(null);

	// Adjust the textarea height dynamically (limit to 5 lines)
	const adjustTextareaHeight = () => {
		//OK
		const textarea = textareaRef.current;
		if (textarea) {
			textarea.style.height = 'auto';
			const lineHeight = parseInt(
				window.getComputedStyle(textarea).lineHeight,
				10
			);
			const maxHeight = lineHeight * 5;
			textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px';
			textarea.style.overflowY =
				textarea.scrollHeight > maxHeight ? 'auto' : 'hidden';
		}
	};

	const handleChange = (e) => {
		//OK
		setMessage(e.target.value);
		adjustTextareaHeight();
	};

	const handleSendClick = () => {
		//OK
		if (message.trim()) {
			onSend(message);
			setMessage('');
			// Reset the textarea height
			if (textareaRef.current) {
				textareaRef.current.style.height = 'auto';
			}
		}
	};

	const handleKeyDown = (e) => {
		//OK
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSendClick();
		}
	};

	return (
		<div className={`create-chat-message-area ${isOpen ? '' : 'hidden'}`}>
			<textarea
				ref={textareaRef}
				value={message}
				onChange={handleChange}
				onKeyDown={handleKeyDown}
				placeholder='Type your message...'
				rows={1}
				className='create-chat-message-input'
			/>
			<div
				style={{
					// minHeight: '100%',
					display: 'flex',
					alignSelf: 'flex-end',
				}}
			>
				<SendButton onClick={handleSendClick} disabled={!message.trim()} />
			</div>
		</div>
	);
}
