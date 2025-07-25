import React from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter, Route, Routes, Link, Switch } from 'react-router-dom';

// import history from './history';
import store from './store';
import { initializeTheme } from './utils/themeUtils';
//Components:

import Dashboard from './components/Dashboard';
import UserLogin from './components/UserLogin';

// Initialize theme before rendering
initializeTheme();

const container = document.getElementById('app');
const root = createRoot(container);
root.render(
	<Provider store={store}>
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<UserLogin />} />
				<Route path='/user/*' element={<Dashboard />} />
			</Routes>
		</BrowserRouter>
	</Provider>
);
