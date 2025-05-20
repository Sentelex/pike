import React from 'react';
import { LuListCollapse } from 'react-icons/lu';

export default function CollapseChatsButton({ onCollapseChats }) {
	return (
		<div id='collapse-chats-button' onClick={onCollapseChats}>
			<div className='button-icon-wrapper'>
				<LuListCollapse />
			</div>
			Fold Chats
		</div>
	);
}
