"""
Filesystem-related tools for the MCP server.
Handles file listing and reading operations.
"""

import os
from typing import List, Optional
from ..config import config
from ..schemas.tool_schemas import (
    GetProjectFilesRequest,
    GetProjectFilesResponse,
    ReadFileRequest,
    ReadFileResponse,
    FileInfo
)


def get_project_files(request: GetProjectFilesRequest) -> GetProjectFilesResponse:
    """
    List files and directories in the project.

    Args:
        request: The request containing parameters for file listing

    Returns:
        GetProjectFilesResponse with file information or error details
    """
    try:
        # Determine the path to list
        base_path = config.PROJECT_PATH
        target_path = base_path

        if request.path:
            target_path = os.path.join(base_path, request.path)
            # Ensure the path is within the project directory
            if not os.path.abspath(target_path).startswith(os.path.abspath(base_path)):
                return GetProjectFilesResponse(
                    success=False,
                    message="Access denied: path outside project directory",
                    files=[]
                )

        if not os.path.exists(target_path):
            return GetProjectFilesResponse(
                success=False,
                message=f"Path does not exist: {request.path or '.'}",
                files=[]
            )

        # List files and directories
        items = []
        for item_name in os.listdir(target_path):
            if not request.include_hidden and item_name.startswith('.'):
                continue

            item_path = os.path.join(target_path, item_name)
            rel_path = os.path.relpath(item_path, base_path)

            # Get file info
            is_dir = os.path.isdir(item_path)
            size = None
            if not is_dir:
                try:
                    size = os.path.getsize(item_path)
                except OSError:
                    size = None

            file_info = FileInfo(
                name=item_name,
                path=rel_path,
                is_directory=is_dir,
                size=size
            )
            items.append(file_info)

        # Sort: directories first, then files, alphabetically
        items.sort(key=lambda x: (not x.is_directory, x.name.lower()))

        return GetProjectFilesResponse(
            success=True,
            message=f"Listed {len(items)} items",
            files=items
        )

    except Exception as e:
        return GetProjectFilesResponse(
            success=False,
            message=f"Error listing files: {str(e)}",
            files=[]
        )


def read_file(request: ReadFileRequest) -> ReadFileResponse:
    """
    Read content from a file.

    Args:
        request: The request containing file path and optional line range

    Returns:
        ReadFileResponse with file content or error details
    """
    try:
        # Construct full path
        base_path = config.PROJECT_PATH
        file_path = os.path.join(base_path, request.file_path)

        # Security check: ensure path is within project directory
        if not os.path.abspath(file_path).startswith(os.path.abspath(base_path)):
            return ReadFileResponse(
                success=False,
                message="Access denied: file outside project directory",
                content="",
                lines_read=0,
                total_lines=0
            )

        if not os.path.exists(file_path):
            return ReadFileResponse(
                success=False,
                message=f"File does not exist: {request.file_path}",
                content="",
                lines_read=0,
                total_lines=0
            )

        if not os.path.isfile(file_path):
            return ReadFileResponse(
                success=False,
                message=f"Path is not a file: {request.file_path}",
                content="",
                lines_read=0,
                total_lines=0
            )

        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        total_lines = len(lines)

        # Handle line range
        start_line = request.start_line or 1
        end_line = request.end_line or total_lines

        # Validate line range
        if start_line < 1 or end_line > total_lines or start_line > end_line:
            return ReadFileResponse(
                success=False,
                message=f"Invalid line range: {start_line}-{end_line} (file has {total_lines} lines)",
                content="",
                lines_read=0,
                total_lines=total_lines
            )

        # Extract requested lines
        selected_lines = lines[start_line-1:end_line]
        content = ''.join(selected_lines)
        lines_read = len(selected_lines)

        return ReadFileResponse(
            success=True,
            message=f"Read {lines_read} lines from {request.file_path}",
            content=content,
            lines_read=lines_read,
            total_lines=total_lines
        )

    except UnicodeDecodeError:
        return ReadFileResponse(
            success=False,
            message=f"Cannot read file: {request.file_path} (binary file or encoding issue)",
            content="",
            lines_read=0,
            total_lines=0
        )
    except Exception as e:
        return ReadFileResponse(
            success=False,
            message=f"Error reading file: {str(e)}",
            content="",
            lines_read=0,
            total_lines=0
        )