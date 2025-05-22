import React, { useState, useEffect } from 'react';
import {
	BrowserRouter,
	Route,
	Routes,
	Link,
	Switch,
	useNavigate,
} from 'react-router-dom';

export default function UserLogin() {
	const navigate = useNavigate();

	const [formData, setFormData] = useState({
		username: '',
		password: '',
	});
	const handleChange = (e) => {
		const { name, value } = e.target;
		setFormData((prevState) => ({
			...prevState,
			[name]: value,
		}));
	};
	const handleLogin = () => {
		navigate('/user/chat');
	};
	return (
		<div id='app-frame'>
			<div id='user-login-page'>
				<div>PIKE</div>
				<div id='user-login-menu'>
					<label className='input-label'>
						<input
							className='input-field'
							type='text'
							name='username' 
							value={formData.username}
							onChange={handleChange}
							placeholder='Username'
						/>

						<input
							className='input-field'
							type='password'
							name='password' 
							value={formData.password}
							onChange={handleChange}
							placeholder='Password'
						/>

						<div id='button-login' onClick={handleLogin}>
							Access PIKE
						</div>
					</label>
				</div>
			</div>
		</div>
	);
}
