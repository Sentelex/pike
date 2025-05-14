// KEEP: using this mock data for testing until have this sent from back end.

export const mockAgentChatLists = [
	{
		agentId: 1,
		chatsList: [
			{ chatId: 'chat-101', chatName: 'Customer A', isOpen: false },
			{ chatId: 'chat-102', chatName: 'Customer B', isOpen: true },
		],
	},
	{
		agentId: 2,
		chatsList: [
			{ chatId: 'chat-201', chatName: 'Customer X', isOpen: false },
			{ chatId: 'chat-202', chatName: 'Customer Y', isOpen: true },
			{ chatId: 'chat-203', chatName: 'Customer Z', isOpen: false },
		],
	},
	{
		agentId: 3,
		chatsList: [{ chatId: 'chat-301', chatName: 'Client 1', isOpen: false }],
	},
	{
		agentId: 4,
		chatsList: [
			{ chatId: 'chat-401', chatName: 'Client A', isOpen: false },
			{ chatId: 'chat-402', chatName: 'Client B', isOpen: false },
			{ chatId: 'chat-403', chatName: 'Client C', isOpen: true },
			{ chatId: 'chat-404', chatName: 'Client D', isOpen: false },
			{ chatId: 'chat-405', chatName: 'Client E', isOpen: false },
			{ chatId: 'chat-406', chatName: 'Client F', isOpen: true },
		],
	},
];

export const mockAgents = [
	{
		agentId: 1,
		agentName: 'Document Assistant',
		developer: 'PIKE',
	},
	{
		agentId: 2,
		agentName: 'Personal Finance Manager',
		developer: 'PIKE',
	},
	{
		agentId: 3,
		agentName: 'Legal Assistant',
		developer: 'PIKE',
	},
	{
		agentId: 4,
		agentName: 'Scheduling Assistant',
		developer: 'PIKE',
	},
];

export const mockPinnedChats = [
	{
		chatId: 1,
		agentId: 2,
		chatName: 'Credit score advice',
		chatAgent: 'Personal Finance Manager',
	},
	{
		chatId: 1,
		agentId: 1,
		chatName: 'Moby Dick Q and A',
		chatAgent: 'Document Assistant',
	},
	{
		chatId: 2,
		agentId: 2,
		chatName: 'Monthly Budget Advice',
		chatAgent: 'Personal Finance Manager',
	},
];
