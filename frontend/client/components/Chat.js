import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleChatOpenThunk, fetchChatHistory } from '../store';

export default function Chat({ agentId, chatName, isOpen, chatId }) {
	const dispatch = useDispatch();
	const chatHistory = useSelector((state) => state.chatHistory[chatId] || []);
	console.log('Chat history:', chatHistory);

	useEffect(() => {
		if (isOpen) {
			dispatch(fetchChatHistory(chatId));
		}
	}, [isOpen, chatId, dispatch]);

	const handleToggle = () => {
		console.log('Click! (handle toggle)');
		dispatch(toggleChatOpenThunk(agentId, chatId));
	};
	return (
		<div className={`chat-window ${isOpen ? 'open' : 'folded'}`}>
			<div
				key={chatId}
				className={`chat-summary ${isOpen ? 'hidden' : ''}`}
				onClick={handleToggle}
			>
				{chatName}
			</div>
			<div
				className={`chat-top-panel ${isOpen ? '' : 'hidden'}`}
				onClick={handleToggle}
			>
				{chatName}
			</div>
			<div className={`chat-viewer ${isOpen ? '' : 'hidden'}`}>
				{isOpen && chatHistory.length > 0
					? chatHistory.map((msg, index) => (
							<div key={index} className='message-test'>
								{typeof msg.content === 'object'
									? msg.content.text
									: msg.content}
							</div>
					  ))
					: isOpen && <div>Loading chat history...</div>}
			</div>
			<div className={`chat-message-input ${isOpen ? '' : 'hidden'}`}>
				Chat message input{' '}
			</div>
		</div>
	);
}
