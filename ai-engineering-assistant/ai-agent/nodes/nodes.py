"""
LangGraph nodes for the AI agent.

Each node represents a step in the agent's workflow.
"""

import json
import os
import requests
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from ..state.state import AgentState
from ..prompts.prompts import TOOL_SELECTION_PROMPT, RESPONSE_SYNTHESIS_PROMPT

# Initialize LLM with OpenRouter
model_name = os.getenv("MODEL_NAME", "openai/gpt-5.5")
llm = ChatOpenAI(
    model=model_name,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

# MCP Server URL - in production, this would be configurable
MCP_SERVER_URL = "http://localhost:8000"


def decide_tool(state: AgentState) -> Dict[str, Any]:
    """
    Decide which tool to call based on the user query.

    This node uses the LLM to analyze the query and select the appropriate tool.
    """
    prompt = PromptTemplate.from_template(TOOL_SELECTION_PROMPT)
    chain = prompt | llm

    result = chain.invoke({"user_query": state.user_query})
    tool_name = result.content.strip().lower()

    # Map tool names to valid options
    valid_tools = {
        "get_recent_commits": "get_recent_commits",
        "get_project_files": "get_project_files",
        "read_file": "read_file"
    }

    selected_tool = valid_tools.get(tool_name, "none")

    return {
        "current_tool": selected_tool,
        "metadata": {**state.metadata, "selected_tool": selected_tool}
    }


def call_tool(state: AgentState) -> Dict[str, Any]:
    """
    Call the selected tool via the MCP server.

    This node makes HTTP requests to the MCP server to execute tools.
    """
    if state.current_tool == "none":
        return {"tool_results": []}

    tool_endpoints = {
        "get_recent_commits": "/tools/get_recent_commits",
        "get_project_files": "/tools/get_project_files",
        "read_file": "/tools/read_file"
    }

    endpoint = tool_endpoints.get(state.current_tool)
    if not endpoint:
        return {
            "tool_results": [],
            "error": f"Unknown tool: {state.current_tool}"
        }

    try:
        # Prepare request payload based on tool
        payload = {}

        if state.current_tool == "get_recent_commits":
            # Simple request - get last 10 commits
            payload = {"limit": 10}
        elif state.current_tool == "get_project_files":
            # Simple request - list root directory
            payload = {}
        elif state.current_tool == "read_file":
            # For read_file, we need to extract a file path from the query
            # This is a simple implementation - in production, use better parsing
            query_lower = state.user_query.lower()
            if "readme" in query_lower:
                payload = {"file_path": "README.md"}
            elif "requirements" in query_lower:
                payload = {"file_path": "requirements.txt"}
            else:
                # Default to README if we can't parse
                payload = {"file_path": "README.md"}

        # Make request to MCP server
        url = f"{MCP_SERVER_URL}{endpoint}"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()

        return {
            "tool_results": [result],
            "metadata": {**state.metadata, "tool_called": state.current_tool}
        }

    except requests.RequestException as e:
        return {
            "tool_results": [],
            "error": f"Failed to call tool {state.current_tool}: {str(e)}"
        }
    except Exception as e:
        return {
            "tool_results": [],
            "error": f"Unexpected error calling tool: {str(e)}"
        }


def synthesize_response(state: AgentState) -> Dict[str, Any]:
    """
    Synthesize the final response based on tool results.

    This node uses the LLM to create a human-readable response from tool outputs.
    """
    if state.error:
        return {"final_response": f"I encountered an error: {state.error}"}

    if not state.tool_results:
        return {"final_response": "I couldn't find a suitable tool to answer your query."}

    # Use LLM to synthesize response
    prompt = PromptTemplate.from_template(RESPONSE_SYNTHESIS_PROMPT)
    chain = prompt | llm

    # Format tool results for the prompt
    tool_results_str = json.dumps(state.tool_results, indent=2)

    result = chain.invoke({
        "user_query": state.user_query,
        "tool_results": tool_results_str
    })

    return {"final_response": result.content}