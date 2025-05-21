import React, { useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router';
import { fetchAgentChatsList, collapseAllChats } from '../store';
import Chat from './Chat';
import CreateChatButton from './CreateChatButton';
import CollapseChatsButton from './CollapseChatsButton';
import { smoothScrollTo } from '../utils/scroll'; // Import the utility

function ChatsWindow() {
	console.log('ChatsWindow');
	const dispatch = useDispatch();

	const { agentId: agentIdParam } = useParams();
	const agentId = agentIdParam;
	const chatLists = useSelector((state) => state.chatLists);
	const agentChatList = chatLists.find((list) => list.agentId === agentId);
	const chatAreaRef = useRef(null);

	const handleScrollToBottom = () => {
		if (chatAreaRef.current) {
			smoothScrollTo(
				chatAreaRef.current,
				chatAreaRef.current.scrollHeight,
				500
			);
		}
	};

	const handleScrollToTop = () => {
		if (chatAreaRef.current) {
			smoothScrollTo(chatAreaRef.current, 0, 50);
		}
	};

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
				key={chat.chatId}
				agentId={agentId}
				chatName={chat.chatName}
				isOpen={chat.isOpen}
				chatId={chat.chatId}
			/>
		));
	};

	const handleCollapseChats = () => {
		dispatch(collapseAllChats(agentId));
		// Wait a short time for state update then scroll to bottom (last chat)
		setTimeout(() => {
			handleScrollToBottom();
		}, 200);
	};

	return (
		<>
			<CreateChatButton
				agentId={agentId}
				handleScrollToBottom={handleScrollToBottom}
			/>
			<CollapseChatsButton onCollapseChats={handleCollapseChats} />
			<div id='top-panel'>
				<div id='filter-menu'>Filter menu</div>
				<div id='chats-search-bar'>Search bar</div>
			</div>
			<div id='main-panel'>
				<div
					id='chat-area'
					key={agentId}
					ref={chatAreaRef}
					style={{ paddingBottom: '50px' }}
				>
					{renderChatList()}
				</div>
			</div>
		</>
	);
}

export default React.memo(ChatsWindow);
