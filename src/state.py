from typing import List, Dict, Optional

class ChatState:
    def __init__(self, chat_id: str, agent_type: str, graph_id: Optional[str] = "default-graph"):
        self.chat_id = chat_id
        self.agent_type = agent_type
        self.graph_id = graph_id
        self.full_messages: List[str] = []
        self.attachment: Optional[str] = None
        self.latest_message: Optional[str] = None

    def add_message(self, message: str, attachment: Optional[str] = None):
        self.latest_message = message
        self.full_messages.append(message)
        if attachment:
            self.attachment = attachment

    def truncate_history(self, limit: int = 10) -> Dict:
        return {
            "graph_id": self.graph_id,
            "full_messages": self.full_messages,
            "attachment": self.attachment,
            "messages": self.full_messages[-limit:]
        }

    def get_state(self) -> Dict:
        return {
            "chat_id": self.chat_id,
            "agent_type": self.agent_type,
            "graph_id": self.graph_id,
            "full_messages": self.full_messages,
            "attachment": self.attachment,
            "latest_message": self.latest_message
        }

    def get_short_state(self) -> Dict:
        short_state = self.truncate_history()
        return short_state
