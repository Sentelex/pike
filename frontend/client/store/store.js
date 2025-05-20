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
const COLLAPSE_ALL_CHATS = 'COLLAPSE_ALL_CHATS'; // New action type

// ACTION CREATORS
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

const toggleChatOpen = (agentId, chatId) => ({
	type: TOGGLE_CHAT_OPEN,
	payload: { agentId, chatId },
});

const setChatHistory = (chatId, messages) => ({
	type: SET_CHAT_HISTORY,
	payload: { chatId, messages },
});

// New action creator to collapse all chats except the most recent one
export const collapseAllChats = (agentId) => ({
	type: COLLAPSE_ALL_CHATS,
	payload: { agentId },
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
	// IN PROGRESS: this will call API to update chat's "isOpen" status:

	// Step 1: Update mock memory in-place
	// const agent = mockAgentChatLists.find((a) => a.agentId === agentId);
	// if (!agent) return;

	// const chat = agent.chatsList.find((c) => c.id === chatId);
	// if (!chat) return;

	// chat.isOpen = !chat.isOpen;

	// Step 2: Dispatch store update
	dispatch(toggleChatOpen(agentId, chatId));
};

export const createNewChat = (userId, agentId, newMessage) => {
	return async (dispatch) => {
		const chatId = generateUUID();
		const message = {
			message: newMessage,
			attachment: null,
		};

		let attempt = 0;
		let response = null;
		const maxAttempts = 3;
		const delay = 2000; // Delay in milliseconds

		while (attempt < maxAttempts) {
			try {
				response = await axios.post(
					`http://localhost:8000/user/${userId}/agent/${agentId}/create_chat/${chatId}`,
					message,
					{ timeout: delay }
				);
				break; // Exit loop on success
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

		if (response) {
			console.log('New chat created response:', response.data);
			// KEEP FOR TESTING: appending chat NOT from response
			dispatch(appendAgentChat(agentId, response.data.newChat));
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

// Agents Reducers
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
				// Collapse all chats except the most recent one
				const updatedChatsList = agent.chatsList.map((chat, index) => {
					if (index < chatsCount - 1) {
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
		default:
			return state;
	}
}
