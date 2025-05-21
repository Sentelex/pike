import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
	toggleChatOpenThunk,
	fetchChatHistory,
	appendChatMessage,
	sendChatMessage,
} from '../store';
import UserMessage from './UserMessage';
import AgentMessage from './AgentMessage';
import ChatMessageInput from './ChatMessageInput';
import { smoothScrollTo } from '../utils/scroll';

function Chat({ agentId, chatName, isOpen, chatId }) {
	console.log('Chat component:', chatId, isOpen);
	const dispatch = useDispatch();
	const chatHistory = useSelector((state) => state.chatHistory[chatId]); // undefined if not fetched
	const chatViewerRef = useRef(null);

	useEffect(() => {
		if (isOpen && !chatHistory) {
			dispatch(fetchChatHistory(chatId));
			console.log('Fetching chat history for chatId:', chatId);
		}
	}, [isOpen, chatId, dispatch, chatHistory]);

	useEffect(() => {
		// Smooth scroll the chat viewer to the bottom whenever chatHistory changes
		if (chatViewerRef.current) {
			smoothScrollTo(
				chatViewerRef.current,
				chatViewerRef.current.scrollHeight,
				500
			);
		}
	}, [chatHistory]);

	const handleToggle = () => {
		console.log('Click! (handle toggle)');
		dispatch(toggleChatOpenThunk(agentId, chatId));
	};

	const handleSendMessage = (message) => {
		dispatch(sendChatMessage(chatId, message));
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
				className='chat-viewer-wrapper'
				style={{
					minHeight: '100%',
					width: '100%',
					display: 'flex',
					flexDirection: 'column',
					justifyContent: 'flex-start',
					alignItems: 'stretch',
					alignSelf: 'stretch',
				}}
			>
				<div
					ref={chatViewerRef}
					className={`chat-viewer ${isOpen ? '' : 'hidden'}`}
					style={{ paddingBottom: '25%', width: '100%' }}
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
			</div>
			{isOpen && (
				<ChatMessageInput isOpen={isOpen} onSendMessage={handleSendMessage} />
			)}
		</div>
	);
}

export default React.memo(Chat);
