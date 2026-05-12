"""
LangGraph workflow definition for the AI agent.

Defines the graph structure and execution flow.
"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any

from ..state.state import AgentState
from ..nodes.nodes import decide_tool, call_tool, synthesize_response


def create_agent_graph() -> StateGraph:
    """
    Create the LangGraph workflow for the AI agent.

    The workflow follows this simple pattern:
    1. Decide which tool to call
    2. Call the tool
    3. Synthesize response

    Returns:
        Configured StateGraph ready for execution
    """
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("decide_tool", decide_tool)
    workflow.add_node("call_tool", call_tool)
    workflow.add_node("synthesize_response", synthesize_response)

    # Define the flow
    workflow.set_entry_point("decide_tool")
    workflow.add_edge("decide_tool", "call_tool")
    workflow.add_edge("call_tool", "synthesize_response")
    workflow.add_edge("synthesize_response", END)

    return workflow


# Create the compiled graph
agent_graph = create_agent_graph().compile()