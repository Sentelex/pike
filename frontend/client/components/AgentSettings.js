import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';

export default function AgentSettings() {
	const { agentId } = useParams();
	const agents = useSelector((state) => state.agents);
	const [currentAgent, setAgent] = useState(false);

	useEffect(() => {
		setAgent(agents.find((agent) => agent.agentId == agentId));
	});

	return (
		<>
			<div id='top-panel'>{currentAgent.agentName} Settings</div>
			<div id='main-panel'></div>
		</>
	);
}
