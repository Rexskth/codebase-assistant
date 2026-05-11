"""
MCP Server - Tool Execution Layer

This is the MCP (Model Context Protocol) server that exposes tools to AI agents.
It handles tool validation, execution, and returns structured responses.

The server does NOT contain any AI reasoning logic - that's handled by the agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import uvicorn

from .config import config
from .schemas.tool_schemas import (
    GetRecentCommitsRequest,
    GetProjectFilesRequest,
    ReadFileRequest
)
from .tools.git_tools import get_recent_commits
from .tools.filesystem_tools import get_project_files, read_file

# Create FastAPI app
app = FastAPI(
    title="MCP Server",
    description="Model Context Protocol Server for AI Engineering Assistant",
    version="1.0.0"
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "MCP Server",
        "version": "1.0.0",
        "description": "Tool execution layer for AI Engineering Assistant",
        "tools": [
            "get_recent_commits",
            "get_project_files",
            "read_file"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/tools/get_recent_commits")
async def api_get_recent_commits(request: GetRecentCommitsRequest):
    """
    Get recent commits from the git repository.

    This endpoint allows AI agents to retrieve recent git commit history.
    """
    try:
        result = get_recent_commits(request)
        return result.dict()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/tools/get_project_files")
async def api_get_project_files(request: GetProjectFilesRequest):
    """
    List files and directories in the project.

    This endpoint allows AI agents to explore the project structure.
    """
    try:
        result = get_project_files(request)
        return result.dict()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/tools/read_file")
async def api_read_file(request: ReadFileRequest):
    """
    Read content from a file.

    This endpoint allows AI agents to read file contents.
    """
    try:
        result = read_file(request)
        return result.dict()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/tools")
async def list_tools():
    """List all available tools."""
    return {
        "tools": [
            {
                "name": "get_recent_commits",
                "description": "Retrieve recent git commits",
                "endpoint": "/tools/get_recent_commits",
                "method": "POST"
            },
            {
                "name": "get_project_files",
                "description": "List project files and directories",
                "endpoint": "/tools/get_project_files",
                "method": "POST"
            },
            {
                "name": "read_file",
                "description": "Read file content",
                "endpoint": "/tools/read_file",
                "method": "POST"
            }
        ]
    }


if __name__ == "__main__":
    # Run the server directly
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True  # Enable auto-reload for development
    )