import React, { useEffect, useState, useRef } from 'react';
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
				200
			);
		}
	};
	// KEEP: alternative scroll function
	// const handleScrollToBottom = () => {
	// 	if (chatAreaRef.current) {
	// 		chatAreaRef.current.scrollTo({
	// 			top: chatAreaRef.current.scrollHeight,
	// 			behavior: 'smooth',
	// 		});
	// 	}
	// };

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
				handleScrollToBottom={handleScrollToBottom}
			/>
			<div id='top-panel'>
				<div id='filter-menu'>Filter menu</div>
				<div id='chats-search-bar'>Search bar</div>
			</div>
			<div id='main-panel'>
				<div id='chat-area' ref={chatAreaRef}>
					{renderChatList()}
				</div>
			</div>
		</>
	);
}
