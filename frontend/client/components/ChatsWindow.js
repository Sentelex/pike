import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router';
import { fetchAgentChatsList } from '../store';
import Chat from './Chat';
import CreateChatButton from './CreateChatButton';
import PopupBlanket from './PopupBlanket';

export default function ChatsWindow() {
	const dispatch = useDispatch();

	const [isCreateChatOpen, setIsCreateChatOpen] = useState(false);
	const [newMessage, setNewMessage] = useState('');
	const { agentId: agentIdParam } = useParams();

	// KEEP FOR TESTING:
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
			<PopupBlanket
				isOpen={isCreateChatOpen}
				setIsOpen={setIsCreateChatOpen}
				newMessage={newMessage}
			/>
			<CreateChatButton
				isOpen={isCreateChatOpen}
				setIsOpen={setIsCreateChatOpen}
				agentId={agentId}
				newMessage={newMessage}
				setNewMessage={setNewMessage}
			/>
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
