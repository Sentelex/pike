import backend.src.graph_builder as gb


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(message.pretty_print() if hasattr(message, "pretty_print") else message)


if __name__ == "__main__":
    model = "Some Model"
    graph = gb.build_graph(model, graph_id="default")

    # Example user input
    user_input = {
        "messages": [
            ("user", "Summarize this: I love langgraph because it's powerful.")
        ],
        "attachment": None,
        "graph_id": "default",
    }

    # Stream the response from the graph, passing the user input
    response = graph.stream(user_input, stream_mode="values")

    print_stream(response)
