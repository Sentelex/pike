import React, { useState, useEffect } from 'react';
import { IoMdSettings } from 'react-icons/io';
import { useNavigate } from 'react-router-dom';

export default function AddNewAgentButton({ onSelect, selected }) {
	const navigate = useNavigate();

	const handleClick = (e) => {
		// e.stopPropagation(); // Stop the click from reaching parent
		navigate('marketplace');
		onSelect('add-agent');
	};

	return (
		<div
			className={`add-new-agent-button ${selected ? 'selected' : ''}`}
			onClick={handleClick}
		>
			+ Add Agent
		</div>
	);
}
