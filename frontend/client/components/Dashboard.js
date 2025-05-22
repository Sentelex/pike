import React, { useState, useEffect } from 'react';
import AgentButton from './AgentButton';
import ChatsWindow from './ChatsWindow';
import AgentSettings from './AgentSettings';
import AgentsMarketplace from './AgentsMarketplace';
import AddNewAgentButton from './AddNewAgentButton';
import UserDashboard from './UserDashboard';
import UserDashboardButton from './UserDashboardButton';
import { useSelector, useDispatch } from 'react-redux';
import { BrowserRouter, Route, Routes, Link, Switch } from 'react-router-dom';
import { fetchUserAgents, fetchPinnedChats } from '../store';

export default function Dashboard() {
	const dispatch = useDispatch();
	const userAgents = useSelector((state) => state.agents);
	const pinnedChats = useSelector((state) => state.pinnedChats);
	const [selectedAgentId, selectAgentId] = useState(null);

	useEffect(() => {
		dispatch(fetchUserAgents(1));
	}, []);

	useEffect(() => {
		dispatch(fetchPinnedChats());
	}, []);

	const renderUserAgents = (userAgents) => {
		return userAgents.length > 0 ? (
			userAgents.map((agent, index) => (
				<AgentButton
					key={index}
					agent={agent}
					onSelect={selectAgentId}
					selected={agent.agentId == selectedAgentId}
				/>
			))
		) : (
			<>no agents</>
		);
	};

	const renderPinnedChats = (pinnedChats) => {
		return pinnedChats.length > 0 ? (
			pinnedChats.map((chat, index) => (
				<div className='pinned-chat-button'>
					{chat.chatName} by {chat.chatAgent}
				</div>
			))
		) : (
			<>no pinned chats</>
		);
	};

	//Actual page:
	return (
		<div id='app-frame'>
			<UserDashboardButton />
			<div key={12} id='left-panel'>
				Left panel
				<AddNewAgentButton
					selected={selectedAgentId === 'add-agent'}
					onSelect={() => selectAgentId('add-agent')}
				/>
				{renderUserAgents(userAgents)}
				<div id='pinned-chats'>Pinned chats:</div>
				{renderPinnedChats(pinnedChats)}
			</div>
			<div id='main-area'>
				<Routes>
					{/* Route for AgentChats */}
					<Route path='agent/:agentId/chat' element={<ChatsWindow />} />
					<Route path='/agent/:agentId/settings' element={<AgentSettings />} />
					<Route path='/marketplace' element={<AgentsMarketplace />} />
					<Route path='/dashboard' element={<UserDashboard />} />
				</Routes>
			</div>
		</div>
	);
}
