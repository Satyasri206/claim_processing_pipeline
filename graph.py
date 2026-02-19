from langgraph.graph import StateGraph, END
from state import GraphState
from agents import (
    segregator_agent,
    id_agent,
    discharge_summary_agent,
    itemized_bill_agent,
)
from aggregator import aggregate


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("segregator", segregator_agent)
    graph.add_node("id_agent", id_agent)
    graph.add_node("discharge_agent", discharge_summary_agent)
    graph.add_node("bill_agent", itemized_bill_agent)
    graph.add_node("aggregator", aggregate)

    graph.set_entry_point("segregator")

 
    graph.add_edge("segregator", "id_agent")
    graph.add_edge("id_agent", "discharge_agent")
    graph.add_edge("discharge_agent", "bill_agent")
    graph.add_edge("bill_agent", "aggregator")

    graph.add_edge("aggregator", END)

    return graph.compile()
