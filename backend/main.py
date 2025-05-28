import uuid as u
import langchain_core.messages as lcm
import backend.src.chat as ct


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(message.pretty_print() if hasattr(
            message, "pretty_print") else message)


if __name__ == "__main__":
    chat = ct.Chat(
        new_message=lcm.HumanMessage(
            content="Summarize this: I love langgraph because it's powerful."),
        messages=[],
        id=u.uuid4(),
        agent_id=u.uuid4(),
    )

    print_stream(ct.get_response(chat_id=chat.id, attachment=None))
