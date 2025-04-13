import tools.stocks as st
import tools.summaries as su
import tools.pdf_files as pf
import tools.text_files as tf
import tools.web_pages as wp
import tools.action_items as aci
from graph_builder import build_default_graph


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(message.pretty_print() if hasattr(message, "pretty_print") else message)


if __name__ == "__main__":
    model = "Some Model"
    tools = [
        st.get_stock_price, 
        su.summarize_text, 
        pf.parse_pdf, 
        tf.parse_file, 
        wp.parse_webpage, 
        aci.get_action_items
    ]
    model = model.bind_tools(tools)  # For models in Langchain

    graph = build_default_graph(model, tools, graph_id="default")

    # Example user input
    user_input = {
        "messages": [("user", "Summarize this: I love langgraph because it's powerful.")],
        "attachment": None,
        "graph_id": "default"
    }

    # Stream the response from the graph, passing the user input
    response = graph.stream(user_input, stream_mode="values")

    print_stream(response)
