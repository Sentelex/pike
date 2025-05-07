import React, { useState, useEffect } from 'react';
import { IoMdSettings } from 'react-icons/io';
import { useNavigate } from 'react-router-dom';

export default function UserDashboardButton() {
	const navigate = useNavigate();

	const handleGoToUserDashboard = (e) => {
		// e.stopPropagation(); // Stop the click from reaching parent
		navigate('dashboard');
	};

	return (
		<div id='user-icon' onClick={handleGoToUserDashboard}>
			A
		</div>
	);
}
