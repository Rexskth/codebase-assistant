"""
State management for the LangGraph agent.

Defines the state schema that flows through the agent's workflow.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AgentState(BaseModel):
    """
    State for the AI agent workflow.

    This state is passed between nodes in the LangGraph workflow.
    It contains the user's query, intermediate results, and final response.
    """

    # User input
    user_query: str = ""

    # Tool execution results
    tool_results: List[Dict[str, Any]] = []

    # Current tool being executed (for tracking)
    current_tool: Optional[str] = None

    # Final response to user
    final_response: str = ""

    # Error information
    error: Optional[str] = None

    # Metadata
    metadata: Dict[str, Any] = {}

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True