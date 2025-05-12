import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router';
import { fetchAgentChatsList } from '../store';
import Chat from './Chat';

export default function ChatsWindow() {
	const dispatch = useDispatch();
	const { agentId: agentIdParam } = useParams();
	// KEEP:
	// const agentId = parseInt(agentIdParam, 10);
	const agentId = agentIdParam;
	console.log('AGENT ID: ', agentId);
	const chatLists = useSelector((state) => state.chatLists);

	const agentChatList = chatLists.find((list) => list.agentId === agentId);

	useEffect(() => {
		if (!agentChatList) {
			dispatch(fetchAgentChatsList(1, agentId));
		}
	}, [agentChatList, agentId, dispatch]);

	const renderChatList = () => {
		if (
			!agentChatList ||
			!agentChatList.chatsList ||
			agentChatList.chatsList.length === 0
		) {
			return <>No chats</>;
		}

		return agentChatList.chatsList.map((chat) => (
			<Chat
				agentId={agentId}
				chatName={chat.chatName}
				isOpen={chat.isOpen}
				chatId={chat.chatId}
			/>
		));
	};

	return (
		<>
			<div id='button-new-chat'>
				New
				<br />
				Chat
			</div>
			<div id='top-panel'>
				<div id='filter-menu'>Filter menu</div>
				<div id='chats-search-bar'>Search bar</div>
			</div>
			<div id='main-panel'>
				<div id='chat-area'>{renderChatList()}</div>
			</div>
		</>
	);
}
