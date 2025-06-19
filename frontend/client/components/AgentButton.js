import React, { useState, useEffect } from 'react';
import { IoMdSettings } from 'react-icons/io';
import { LuSettings2 } from 'react-icons/lu';
import { useNavigate } from 'react-router-dom';

export default function AgentButton({ agent, selected, onSelect }) {
	const navigate = useNavigate();
	const [hovered, setHovered] = useState(false);

	const handleGoToAgentSettings = (e) => {
		e.stopPropagation(); // Stop the click from reaching parent
		navigate(`agent/${agent.agentId}/settings`);
	};
	const handleClick = () => {
		navigate(`agent/${agent.agentId}/chat`);
		onSelect(agent.agentId);
	};

	return (
		<div className='agent-button-wrapper'>
			<div
				className={`agent-button ${selected ? 'selected' : ''}`}
				onMouseEnter={() => setHovered(true)}
				onMouseLeave={() => setHovered(false)}
				onClick={handleClick}
			>
				<img
					src='/agent-icon-2.png'
					style={{ height: '45px', width: '45px' }}
				/>
				<div className='a-b-name'>
					<span>{agent.agentName}</span>
				</div>
				{hovered ? (
					<div className='a-b-settings' onClick={handleGoToAgentSettings}>
						<LuSettings2 />
					</div>
				) : (
					''
					// <div className='a-b-settings'></div>
				)}
			</div>
		</div>
	);
}
