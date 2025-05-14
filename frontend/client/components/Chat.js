import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { toggleChatOpenThunk } from '../store';

export default function Chat({ agentId, chatName, isOpen, chatId }) {
	const dispatch = useDispatch();

	const handleToggle = () => {
		console.log('Click! (handle toggle)');
		dispatch(toggleChatOpenThunk(agentId, chatId));
	};
	return (
		<div className={`chat-window ${isOpen ? 'open' : 'folded'}`}>
			<div
				key={chatId}
				className={`chat-window-folded ${isOpen ? 'hidden' : ''}`}
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
				{/* KEEP WHILE BEING BUILT, defines fields: */}
				{/* Chat viewer */}
				{/* {generateDivs(15, 'message-test')} */}
				{[...Array(15)].map((_, i) => (
					<div className='message-test' key={i}>
						Hello Pike and Hello world!
					</div>
				))}
			</div>
			<div className={`chat-message-input ${isOpen ? '' : 'hidden'}`}>
				Chat message input{' '}
			</div>
		</div>
	);
}
