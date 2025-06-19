import React from 'react';
import { TbMoodPlus } from 'react-icons/tb';
import { useNavigate } from 'react-router-dom';

export default function AddNewAgentButton({ onSelect, selected }) {
	const navigate = useNavigate();

	const handleClick = (e) => {
		navigate('marketplace');
		onSelect('add-agent');
	};

	return (
		<div className='agent-button-wrapper'>
			<div
				className={`add-new-agent-button ${selected ? 'selected' : ''}`}
				onClick={handleClick}
			>
				<div className='agent-icon-wrapper'>
					<TbMoodPlus style={{ fontSize: 'x-large' }} />
				</div>
				<div className='a-b-name'>
					<span>Add Agent</span>
				</div>
			</div>
		</div>
	);
}
