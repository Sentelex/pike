import React from 'react';
import { useTheme } from '../utils/themeUtils';

const ThemeToggle = () => {
	const { theme, toggleTheme, isDark } = useTheme();

	return (
		<button
			className="theme-toggle"
			onClick={toggleTheme}
			title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
			aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
		>
			{isDark ? '☀️' : '🌙'}
		</button>
	);
};

export default ThemeToggle;
