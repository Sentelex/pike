import React, { useEffect, useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router';
import { fetchAgentChatsList, collapseAllChats } from '../store';
import Chat from './Chat';
import CreateChatButton from './CreateChatButton';
import PopupBlanket from './PopupBlanket';
import CollapseChatsButton from './CollapseChatsButton';

export default function ChatsWindow() {
	const dispatch = useDispatch();

	const [isCreateChatOpen, setIsCreateChatOpen] = useState(false);
	const [newMessage, setNewMessage] = useState('');
	const { agentId: agentIdParam } = useParams();
	// KEEP FOR TESTING:
	// const agentId = parseInt(agentIdParam, 10);
	const agentId = agentIdParam;
	const chatLists = useSelector((state) => state.chatLists);
	const agentChatList = chatLists.find((list) => list.agentId === agentId);
	const chatAreaRef = useRef(null);

	const easeInOutQuad = (t) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t);

	const smoothScrollTo = (element, target, duration = 200) => {
		const start = element.scrollTop;
		const change = target - start;
		const startTime = performance.now();

		const animateScroll = (currentTime) => {
			const elapsed = currentTime - startTime;
			const progress = Math.min(elapsed / duration, 1);
			const easedProgress = easeInOutQuad(progress);
			element.scrollTop = start + change * easedProgress;
			if (progress < 1) {
				requestAnimationFrame(animateScroll);
			}
		};
		requestAnimationFrame(animateScroll);
	};

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
		// handleScrollToTop();
		// Wait a short time for state update then scroll to bottom (last chat)
		setTimeout(() => {
			handleScrollToBottom();
		}, 200);
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
