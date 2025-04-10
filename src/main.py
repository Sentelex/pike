import state as s
import router as r

class LangGraphApp:
    def __init__(self):
        self.graph = self.build_graph()
        self.llm_orchestrator = r.LLMOrchestrater()

    def build_graph(self):
        # Build the graph logic, if needed.
        return {}

    def final_response(self, state):
        return state["response"]

    def invoke(self, message):
        # Combine the pieces: create a state, pass it to the orchestrator, and get a response.
        chat_state = s.ChatState(chat_id="unique_id", agent_type="chatbot")
        chat_state.add_message(message)
        short_state = chat_state.get_short_state()

        # Render the prompt based on the state
        response = self.llm_orchestrator.get_response(short_state)
        return self.final_response(response)