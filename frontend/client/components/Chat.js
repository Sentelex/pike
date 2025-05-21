import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleChatOpenThunk, fetchChatHistory } from '../store';
import UserMessage from './UserMessage';
import AgentMessage from './AgentMessage';
import ChatMessageInput from './ChatMessageInput';

function Chat({ agentId, chatName, isOpen, chatId }) {
	console.log('Chat component:', chatId, isOpen);
	const dispatch = useDispatch();
	const chatHistory = useSelector((state) => state.chatHistory[chatId]); // undefined if not fetched

	useEffect(() => {
		if (isOpen && !chatHistory) {
			dispatch(fetchChatHistory(chatId));
			console.log('Fetching chat history for chatId:', chatId);
		}
	}, [isOpen, chatId, dispatch, chatHistory]);

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
			<div
				className={`chat-viewer ${isOpen ? '' : 'hidden'}`}
				style={{ paddingBottom: '25%' }}
			>
				{isOpen && chatHistory && chatHistory.length > 0
					? chatHistory.map((message, index) => {
							switch (message.type) {
								case 'human': {
									return (
										<div key={index} className='message-wrapper user'>
											<UserMessage message={message} />
										</div>
									);
								}
								case 'ai': {
									return (
										<div key={index} className='message-wrapper agent'>
											<AgentMessage message={message} />
										</div>
									);
								}
								default:
									return null;
							}
					  })
					: isOpen && <div>Loading chat history...</div>}
			</div>
			{isOpen && (
				<ChatMessageInput
					isOpen={isOpen}
					onSend={(msg) => {
						console.log('Send message:', msg);
						// perform your send action here, e.g., dispatch(createMessage(...))
					}}
				/>
			)}
		</div>
	);
}

export default React.memo(Chat);
