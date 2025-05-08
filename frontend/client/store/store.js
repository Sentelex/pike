import axios from 'axios';
import { mockAgentChatLists } from './mockData';

// ACTION TYPES

// Issue Action Types
const SET_USER_AGENTS = 'SET_USER_AGENTS';
const SET_PINNED_CHATS = 'SET_PINNED_CHATS';
const ADD_AGENT_CHATS_LIST = 'ADD_AGENT_CHATS_LIST';
const APPEND_AGENT_CHAT = 'APPEND_AGENT_CHAT';
const TOGGLE_CHAT_OPEN = 'TOGGLE_CHAT_OPEN';

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

//THUNK CREATORS

// Fetch all active user agents
export const fetchUserAgents = (userId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/agents`
		);
		console.log('USER AGENTS:', data);
		// const data = [
		// 	{
		// 		agentId: 1,
		// 		agentName: 'Document Assistant',
		// 		developer: 'PIKE',
		// 	},
		// 	{
		// 		agentId: 2,
		// 		agentName: 'Personal Finance Manager',
		// 		developer: 'PIKE',
		// 	},
		// 	{
		// 		agentId: 3,
		// 		agentName: 'Legal Assistant',
		// 		developer: 'PIKE',
		// 	},
		// 	{
		// 		agentId: 4,
		// 		agentName: 'Scheduling Assistant',
		// 		developer: 'PIKE',
		// 	},
		// ];

		dispatch(setUserAgents(data));
	};
};

export const fetchPinnedChats = (userId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/pinned-chats`
		);
		// const data = [
		// 	{
		// 		chatId: 1,
		// 		agentId: 2,
		// 		chatName: 'Credit score advice',
		// 		chatAgent: 'Personal Finance Manager',
		// 	},
		// 	{
		// 		chatId: 1,
		// 		agentId: 1,
		// 		chatName: 'Moby Dick Q and A',
		// 		chatAgent: 'Document Assistant',
		// 	},
		// 	{
		// 		chatId: 2,
		// 		agentId: 2,
		// 		chatName: 'Monthly Budget Advice',
		// 		chatAgent: 'Personal Finance Manager',
		// 	},
		// ];

		dispatch(setPinnedChats(data));
	};
};

export const fetchAgentChatsList = (userId, agentId) => {
	return async (dispatch) => {
		const { data } = await axios.get(
			`http://localhost:8000/user/${userId}/agent/${agentId}/chats`
		);
		// const data = mockAgentChatLists.find((item) => item.agentId === agentId);
		console.log('THIS SHOULD BE CHATS LIST', data);

		dispatch(addAgentChatsList({ agentId: agentId, chatsList: data }));
	};
};

export const toggleChatOpenThunk = (agentId, chatId) => (dispatch) => {
	// Step 1: Update mock memory in-place
	// const agent = mockAgentChatLists.find((a) => a.agentId === agentId);
	// if (!agent) return;

	// const chat = agent.chatsList.find((c) => c.id === chatId);
	// if (!chat) return;

	// chat.isOpen = !chat.isOpen;

	// Step 2: Dispatch store update
	dispatch(toggleChatOpen(agentId, chatId));
};

// OLD
// // Fetch a card and its contents
// export const fetchCard = (cardId, cardType) => {
// 	return async (dispatch) => {
// 		try {
// 			switch (cardType) {
// 				case 'newsCard':
// 					const { data } = await axios.get(`/api/newscards/${cardId}`);
// 					dispatch(setCard(data, 'newsCard'));
// 			}
// 		} catch (error) {
// 			console.error('Error fetching card and contents:', error);
// 			// Dispatch an error action if the API call fails
// 			dispatch(setCardWContentError('Failed to fetch card and contents.'));
// 		}
// 	};
// };
// // Update a text
// export const updateText = (textId, existing, newText) => {
// 	return async (dispatch) => {
// 		const { data } = await axios.put(`/api/texts/${textId}`, {
// 			text: newText, // assuming newText has the text and other fields
// 			order: existing.order,
// 			active: existing.active,
// 			locked: existing.locked,
// 		});
// 		dispatch(updateTextAction(data));
// 	};
// };

// // Create a staff member
// export const createStaffMember = (staff) => {
// 	return async (dispatch) => {
// 		const { data } = await axios.post('/api/staff', staff);
// 		dispatch(createStaff(data));
// 	};
// };

// // Delete a staff member by ID
// export const deleteStaffMember = (id) => {
// 	return async (dispatch) => {
// 		await axios.delete(`/api/staff/${id}`);
// 		dispatch(deleteStaff(id));
// 	};
// };

// Agents Reducers
export function agents(state = [], action) {
	switch (action.type) {
		case SET_USER_AGENTS:
			return action.payload;
		// case UPDATE_TEXT:
		// 	return state.map((item) =>
		// 		item.id === action.payload.id ? { ...item, ...action.payload } : item
		// 	);
		// case ADD_TEXT:
		// 	return [...state, action.payload];
		// case DELETE_TEXT:
		// 	return state.filter((text) => text.id !== action.payload);
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

// export function chatLists(state = [], action) {
// 	switch (action.type) {
// 		case ADD_AGENT_CHATS_LIST:
// 			return state.some((agent) => agent.agentId === action.payload.agentId)
// 				? state.map((agent) =>
// 						agent.agentId === action.payload.agentId
// 							? action.payload // Replace the whole agent object
// 							: agent
// 				  )
// 				: [...state, action.payload]; // Add the new agent if not present

// 		default:
// 			return state;
// 	}
// }

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

		default:
			return state;
	}
}
