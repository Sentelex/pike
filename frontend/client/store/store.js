import axios from 'axios';
import { mockAgentChatLists, mockAgents, mockPinnedChats } from './mockData';
import { v4 as uuidv4 } from 'uuid';

const generateUUID = () => uuidv4();

// ACTION TYPES
const SET_USER_AGENTS = 'SET_USER_AGENTS';
const SET_PINNED_CHATS = 'SET_PINNED_CHATS';
const ADD_AGENT_CHATS_LIST = 'ADD_AGENT_CHATS_LIST';
const APPEND_AGENT_CHAT = 'APPEND_AGENT_CHAT';
const TOGGLE_CHAT_OPEN = 'TOGGLE_CHAT_OPEN';
const UPDATE_NEW_CHAT_MESSAGE = 'UPDATE_NEW_CHAT_MESSAGE';
const SET_CHAT_HISTORY = 'SET_CHAT_HISTORY';
const COLLAPSE_ALL_CHATS = 'COLLAPSE_ALL_CHATS';
const APPEND_CHAT_MESSAGE = 'APPEND_CHAT_MESSAGE';

// ACTION CREATORS
const UPDATE_AGENT_CHAT = 'UPDATE_AGENT_CHAT';

const setUserAgents = (userAgents) => ({
	type: SET_USER_AGENTS,
	payload: userAgents,
});

const setPinnedChats = (pinnedChats) => ({
	type: SET_PINNED_CHATS,
	payload: pinnedChats,
});
const addAgentChatsList = (agentChatsList) => ({
	type: ADD_AGENT_CHATS_LIST,
	payload: agentChatsList,
});

const appendAgentChat = (agentId, newChat) => ({
	type: APPEND_AGENT_CHAT,
	payload: { agentId, newChat },
});

const updateAgentChat = (agentId, updatedChat) => ({
	type: UPDATE_AGENT_CHAT,
	payload: { agentId, updatedChat },
});

const toggleChatOpen = (agentId, chatId) => ({
	type: TOGGLE_CHAT_OPEN,
	payload: { agentId, chatId },
});

const setChatHistory = (chatId, messages) => ({
	type: SET_CHAT_HISTORY,
	payload: { chatId, messages },
});

// Collapse all chats except the most recent one
export const collapseAllChats = (agentId) => ({
	type: COLLAPSE_ALL_CHATS,
	payload: { agentId },
});

export const appendChatMessage = (chatId, message) => ({
	type: APPEND_CHAT_MESSAGE,
	payload: { chatId, message },
});

//THUNK CREATORS

// Fetch all active user agents
export const fetchUserAgents = (userId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/agents`
		);
		// KEEP FOR TESTING
		// const data = mockAgents;
		// console.log('USER AGENTS:', data);
		dispatch(setUserAgents(data));
	};
};

export const fetchPinnedChats = (userId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/pinned-chats`
		);
		// KEEP FOR TESTING
		// const data = mockPinnedChats;
		// console.log('PINNED CHATS:', data);

		dispatch(setPinnedChats(data));
	};
};

export const fetchAgentChatsList = (userId, agentId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/agent/${agentId}/chats`
		);
		// KEEP FOR TESTING:
		// const data = mockAgentChatLists.find(
		// 	(item) => item.agentId === agentId
		// ).chatsList;

		console.log('THIS SHOULD BE CHATS LIST', data);

		dispatch(addAgentChatsList({ agentId: agentId, chatsList: data }));
	};
};

export const toggleChatOpenThunk = (agentId, chatId) => (dispatch) => {
	dispatch(toggleChatOpen(agentId, chatId));
};

export const createNewChat = (userId, agentId, newMessage) => {
	return async (dispatch) => {
		const chatId = generateUUID();
		const optimisticChat = {
			chatId: chatId,
			agentId: agentId,
			chatName: '...',
			isBookmarked: false,
			isOpen: true,
			isPinned: false,
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		};
		const optimisticMessage = {
			content: newMessage,
			type: 'human',
		};
		console.log('Optimistic chat:', optimisticChat);

		// Optimistically add the chat to both chatLists and chatHistory
		dispatch(appendAgentChat(agentId, optimisticChat));
		dispatch(setChatHistory(chatId, [optimisticMessage]));

		let attempt = 0;
		let response = null;
		const maxAttempts = 3;
		const delay = 2000;

		while (attempt < maxAttempts) {
			try {
				response = await axios.post(
					`http://localhost:8000/user/${userId}/agent/${agentId}/create_chat/${chatId}`,
					{ message: newMessage, attachment: null },
					{ timeout: delay }
				);
				break;
			} catch (error) {
				attempt++;
				console.error(`Attempt ${attempt} failed:`, error.message);
				if (attempt === maxAttempts) {
					console.error(
						`Failed to create new chat after ${maxAttempts} attempts.`
					);
					return;
				}
			}
		}

		// Update the optimistic chat with response data if available
		if (response) {
			console.log('New chat created response:', response.data);
			dispatch(updateAgentChat(agentId, response.data.newChat));
			dispatch(
				setChatHistory(chatId, [optimisticMessage, response.data.message] || [])
			);
		}
	};
};

export const fetchChatHistory = (chatId) => {
	return async (dispatch) => {
		try {
			const { data } = await axios.get(
				`http://localhost:8000/chat/${chatId}/history`
			);
			// Assuming data is an array of message objects
			dispatch(setChatHistory(chatId, data.messages));
			console.log('Chat history fetched:', data);
		} catch (error) {
			console.error('Failed to fetch chat history:', error);
		}
	};
};

export const sendChatMessage = (chatId, message) => {
	return async (dispatch) => {
		// Optimistically add the user's new message to the history
		const newUserMessage = {
			type: 'human',
			content: message,
		};
		dispatch(appendChatMessage(chatId, newUserMessage));

		try {
			const { data } = await axios.post(
				`http://localhost:8000/chat/${chatId}/response`,
				{ message, attachment: null }
			);
			console.log('Response to new Message:', data);
			if (data) {
				dispatch(appendChatMessage(chatId, data));
			}
		} catch (error) {
			console.error('Failed to send chat message:', error);
		}
	};
};

// Reducers
export function agents(state = [], action) {
	switch (action.type) {
		case SET_USER_AGENTS:
			return action.payload;
		default:
			return state;
	}
}

export function pinnedChats(state = [], action) {
	switch (action.type) {
		case SET_PINNED_CHATS:
			return action.payload;
		default:
			return state;
	}
}

const MAX_CHAT_LISTS = 2;

export function chatLists(state = [], action) {
	switch (action.type) {
		case ADD_AGENT_CHATS_LIST: {
			const { agentId, chatsList } = action.payload;
			const filtered = state.filter((item) => item.agentId !== agentId);
			const trimmed =
				filtered.length >= MAX_CHAT_LISTS ? filtered.slice(1) : filtered;
			return [...trimmed, { agentId, chatsList }];
		}

		case APPEND_AGENT_CHAT: {
			const { agentId, newChat } = action.payload;
			return state.map((item) => {
				if (item.agentId === agentId) {
					return {
						...item,
						chatsList: [...item.chatsList, newChat],
					};
				}
				return item;
			});
		}

		// Update an optimistic chat with final data
		case UPDATE_AGENT_CHAT: {
			const { agentId, updatedChat } = action.payload;
			return state.map((item) => {
				if (item.agentId !== agentId) return item;
				return {
					...item,
					chatsList: item.chatsList.map((chat) =>
						chat.chatId === updatedChat.chatId ? updatedChat : chat
					),
				};
			});
		}

		case TOGGLE_CHAT_OPEN: {
			const { agentId, chatId } = action.payload;
			console.log('State update: toggle chat open', agentId, chatId);
			return state.map((agent) => {
				if (agent.agentId !== agentId) return agent;

				return {
					...agent,
					chatsList: agent.chatsList.map((chat) =>
						chat.chatId === chatId ? { ...chat, isOpen: !chat.isOpen } : chat
					),
				};
			});
		}

		case COLLAPSE_ALL_CHATS: {
			const { agentId } = action.payload;
			return state.map((agent) => {
				if (agent.agentId !== agentId) return agent;
				if (!agent.chatsList || agent.chatsList.length === 0) return agent;
				const chatsCount = agent.chatsList.length;
				const popLastChat = 0;
				// 1 = Collapse all but the last chat
				// 0 = Collapse all chats
				const updatedChatsList = agent.chatsList.map((chat, index) => {
					if (index < chatsCount - popLastChat) {
						return { ...chat, isOpen: false };
					}
					return chat;
				});
				return { ...agent, chatsList: updatedChatsList };
			});
		}

		default:
			return state;
	}
}

export function newChatMessage(state = '', action) {
	switch (action.type) {
		case UPDATE_NEW_CHAT_MESSAGE:
			return action.payload;
		default:
			return state;
	}
}

export function chatHistory(state = {}, action) {
	switch (action.type) {
		case SET_CHAT_HISTORY: {
			const { chatId, messages } = action.payload;
			return {
				...state,
				[chatId]: messages,
			};
		}
		case APPEND_CHAT_MESSAGE: {
			const { chatId, message } = action.payload;
			const existingMessages = state[chatId] || [];
			return {
				...state,
				[chatId]: [...existingMessages, message],
			};
		}
		default:
			return state;
	}
}
