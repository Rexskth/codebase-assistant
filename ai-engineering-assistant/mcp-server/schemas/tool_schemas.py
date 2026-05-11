"""
Pydantic schemas for MCP tool requests and responses.
Defines structured input/output models for all tools.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# Base response model
class ToolResponse(BaseModel):
    """Base response model for all tool executions."""
    success: bool = Field(..., description="Whether the tool execution was successful")
    message: str = Field(..., description="Human-readable message about the result")
    data: Optional[dict] = Field(None, description="Structured data returned by the tool")


# get_recent_commits tool
class GetRecentCommitsRequest(BaseModel):
    """Request model for get_recent_commits tool."""
    limit: int = Field(10, description="Number of recent commits to retrieve", ge=1, le=100)
    since_days: Optional[int] = Field(None, description="Only commits from the last N days", ge=1)


class CommitInfo(BaseModel):
    """Information about a git commit."""
    hash: str = Field(..., description="Commit hash")
    author: str = Field(..., description="Commit author")
    date: str = Field(..., description="Commit date")
    message: str = Field(..., description="Commit message")


class GetRecentCommitsResponse(ToolResponse):
    """Response model for get_recent_commits tool."""
    data: Optional[dict] = Field(None, description="Commit data")
    # Override data to be more specific
    commits: List[CommitInfo] = Field(default_factory=list, description="List of recent commits")


# get_project_files tool
class GetProjectFilesRequest(BaseModel):
    """Request model for get_project_files tool."""
    path: Optional[str] = Field(None, description="Subpath within the project to list files from")
    include_hidden: bool = Field(False, description="Whether to include hidden files (starting with .)")


class FileInfo(BaseModel):
    """Information about a file or directory."""
    name: str = Field(..., description="File or directory name")
    path: str = Field(..., description="Full path relative to project root")
    is_directory: bool = Field(..., description="Whether this is a directory")
    size: Optional[int] = Field(None, description="File size in bytes (None for directories)")


class GetProjectFilesResponse(ToolResponse):
    """Response model for get_project_files tool."""
    files: List[FileInfo] = Field(default_factory=list, description="List of files and directories")


# read_file tool
class ReadFileRequest(BaseModel):
    """Request model for read_file tool."""
    file_path: str = Field(..., description="Path to the file to read, relative to project root")
    start_line: Optional[int] = Field(None, description="Starting line number (1-based)", ge=1)
    end_line: Optional[int] = Field(None, description="Ending line number (1-based)", ge=1)


class ReadFileResponse(ToolResponse):
    """Response model for read_file tool."""
    content: str = Field("", description="File content")
    lines_read: int = Field(0, description="Number of lines read")
    total_lines: int = Field(0, description="Total lines in the file")