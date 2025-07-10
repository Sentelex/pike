import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setTheme, toggleTheme } from '../store';

// Custom hook for theme management
export const useTheme = () => {
	const theme = useSelector((state) => state.theme);
	const dispatch = useDispatch();

	const setCurrentTheme = (newTheme) => {
		dispatch(setTheme(newTheme));
	};

	const toggleCurrentTheme = () => {
		dispatch(toggleTheme());
	};

	// Apply theme to document root
	useEffect(() => {
		document.documentElement.setAttribute('data-theme', theme);
		
		// Store theme preference in localStorage
		localStorage.setItem('theme', theme);
	}, [theme]);

	// Load theme from localStorage on mount
	useEffect(() => {
		const savedTheme = localStorage.getItem('theme');
		if (savedTheme && savedTheme !== theme) {
			dispatch(setTheme(savedTheme));
		}
	}, [dispatch, theme]);

	return {
		theme,
		setTheme: setCurrentTheme,
		toggleTheme: toggleCurrentTheme,
		isDark: theme === 'dark',
		isLight: theme === 'light',
	};
};

// Theme initialization utility
export const initializeTheme = () => {
	// Check for saved theme preference or default to dark
	const savedTheme = localStorage.getItem('theme') || 'dark';
	document.documentElement.setAttribute('data-theme', savedTheme);
	return savedTheme;
};
