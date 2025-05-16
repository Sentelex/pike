import { createStore, combineReducers, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import thunkMiddleware from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import {
	agents,
	pinnedChats,
	chatLists,
	newChatMessage,
	chatHistory,
} from './store';

const reducer = combineReducers({
	agents,
	pinnedChats,
	chatLists,
	newChatMessage,
	chatHistory,
});
const middleware = composeWithDevTools(
	applyMiddleware(thunkMiddleware, createLogger({ collapsed: true }))
);
const store = createStore(reducer, middleware);

export default store;
export * from './store';
