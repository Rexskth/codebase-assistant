"""
AI Agent - Reasoning and Orchestration Layer

This is the LangGraph agent that understands user queries and orchestrates tool calls.
It runs via CLI and communicates with the MCP server for tool execution.

The agent does NOT directly access external systems - all interactions go through MCP tools.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Map OpenRouter API key to OpenAI API key for LangChain compatibility
if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# Check for required API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY environment variable is required")
    print("Please create a .env file with your OpenRouter API key")
    print("Get your key from: https://openrouter.ai")
    sys.exit(1)

from .graph.graph import agent_graph
from .state.state import AgentState

# Map OpenRouter API key to OpenAI API key for LangChain compatibility
if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# Check for required API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY environment variable is required")
    print("Please create a .env file with your OpenRouter API key")
    print("Get your key from: https://openrouter.ai")
    sys.exit(1)


def run_agent_query(user_query: str) -> str:
    """
    Run the agent workflow for a user query.

    Args:
        user_query: The user's natural language query

    Returns:
        The agent's response
    """
    # Create initial state
    initial_state = AgentState(user_query=user_query)

    # Run the graph using a plain dict input
    try:
        result = agent_graph.invoke(initial_state.dict())

        # Return the final response
        return result.get("final_response", "No response generated")

    except Exception as e:
        return f"Error running agent: {str(e)}"


def cli_interface():
    """Command-line interface for the AI agent."""
    print("🤖 AI Engineering Assistant (Version 1)")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 50)

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break

            if not user_input:
                continue

            # Process the query
            print("🤔 Thinking...")
            response = run_agent_query(user_input)

            # Display response
            print(f"\nAssistant: {response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    # Check if MCP server is running
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("⚠️  Warning: MCP server health check failed")
            print("Make sure the MCP server is running on http://localhost:8000")
    except:
        print("⚠️  Warning: Cannot connect to MCP server")
        print("Make sure the MCP server is running on http://localhost:8000")
        print("Starting agent anyway...")

    # Start CLI
    cli_interface()