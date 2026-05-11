# AI Engineering Assistant Platform

A production-style AI engineering assistant platform built incrementally using MCP, LangGraph, and modern Python practices.

## Project Vision

This project builds a modular AI infrastructure platform for software engineering assistance, focusing on:

- **Modular Architecture**: Separate MCP server for tool execution and LangGraph agent for orchestration
- **Production-Ready**: Observable, secure, and maintainable design
- **Incremental Development**: Version-by-version implementation with clear milestones

## Current Version: Version 1 - Basic MCP + Agent

### Features
- MCP server exposing basic tools (git, filesystem)
- LangGraph agent for simple tool orchestration
- CLI interface for interaction
- Clean separation of concerns

### Tools Available
- `get_recent_commits`: Retrieve recent git commits
- `get_project_files`: List project files
- `read_file`: Read file contents

### Architecture

#### MCP Server (`mcp-server/`)
- **Purpose**: Tool execution layer
- **Tech**: FastAPI, Pydantic
- **Responsibilities**:
  - Expose tools via REST API
  - Validate requests
  - Execute tools safely
  - Return structured responses

#### AI Agent (`ai-agent/`)
- **Purpose**: Reasoning and orchestration layer
- **Tech**: LangGraph, LangChain
- **Responsibilities**:
  - Understand user queries
  - Decide which tools to call
  - Orchestrate workflows
  - Synthesize responses

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- OpenRouter API Key (get one at https://openrouter.ai)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-engineering-assistant
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

Example `.env`:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
MODEL_NAME=openai/gpt-5.5
```

3. Install dependencies for MCP server:
```bash
cd mcp-server
pip install -r requirements.txt
```

4. Install dependencies for AI agent:
```bash
cd ../ai-agent
pip install -r requirements.txt
```

### Running the System

1. **Start the MCP server** (in terminal 1):
```bash
cd mcp-server
python main.py
```
The server will start on http://localhost:8000

2. **Start the AI agent** (in terminal 2):
```bash
cd ai-agent
python main.py
```

### Example Usage

The agent accepts natural language queries:

```
What changed today?
Show authentication files
Summarize recent commits
```

Example interaction:
```
You: What changed today?
🤔 Thinking...

Assistant: Here are the recent commits from today:

1. **fix: update error handling in auth module**
   - Author: John Doe
   - Date: 2024-01-15T10:30:00
   - Fixed null pointer exception in login flow

2. **feat: add user profile endpoint**
   - Author: Jane Smith
   - Date: 2024-01-15T09:15:00
   - Added GET /api/user/profile with basic user info
```

### Architecture Overview

#### MCP Server (`mcp-server/`)
- **Framework**: FastAPI with Pydantic
- **Purpose**: Tool execution layer
- **Tools**:
  - `get_recent_commits`: Git commit history
  - `get_project_files`: File system exploration
  - `read_file`: File content reading

#### AI Agent (`ai-agent/`)
- **Framework**: LangGraph + LangChain
- **Purpose**: Query understanding and orchestration
- **Workflow**: Query → Tool Selection → Tool Execution → Response Synthesis

## Development Philosophy

- **Incremental**: Build version-by-version, keeping each version stable
- **Modular**: Clean separation between components
- **Production-Oriented**: Focus on maintainability, observability, and security
- **Educational**: Learn MCP architecture and agent orchestration patterns

## Version Roadmap

- **Version 1**: Basic MCP + Agent (Current)
- **Version 2**: Memory + Context
- **Version 3**: Stateful Workflows
- **Version 4**: Observability + Monitoring
- **Version 5**: Structured Logging + Tracing
- **Version 6**: Authentication + Authorization
- **Version 7**: Reliability Engineering
- **Version 8**: Multi-Agent System
- **Version 9**: Frontend Dashboard

## Contributing

This project follows incremental development. Please focus on the current version only.

## License

[Add license information]