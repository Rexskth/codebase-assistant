"""
Git-related tools for the MCP server.
Handles git operations like retrieving commits.
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional
from git import Repo, GitCommandError
from ..config import config
from ..schemas.tool_schemas import (
    GetRecentCommitsRequest,
    GetRecentCommitsResponse,
    CommitInfo
)


def get_recent_commits(request: GetRecentCommitsRequest) -> GetRecentCommitsResponse:
    """
    Retrieve recent commits from the git repository.

    Args:
        request: The request containing parameters for commit retrieval

    Returns:
        GetRecentCommitsResponse with commit information or error details
    """
    try:
        # Initialize git repo
        repo_path = config.PROJECT_PATH
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return GetRecentCommitsResponse(
                success=False,
                message="No git repository found in the project path",
                commits=[]
            )

        repo = Repo(repo_path)

        # Calculate since date if specified
        since_date = None
        if request.since_days:
            since_date = datetime.now() - timedelta(days=request.since_days)

        # Get commits
        commits = list(repo.iter_commits(
            max_count=request.limit,
            since=since_date
        ))

        # Convert to CommitInfo objects
        commit_infos = []
        for commit in commits:
            commit_info = CommitInfo(
                hash=commit.hexsha,
                author=str(commit.author),
                date=commit.committed_datetime.isoformat(),
                message=commit.message.strip()
            )
            commit_infos.append(commit_info)

        return GetRecentCommitsResponse(
            success=True,
            message=f"Retrieved {len(commit_infos)} commits",
            commits=commit_infos
        )

    except GitCommandError as e:
        return GetRecentCommitsResponse(
            success=False,
            message=f"Git error: {str(e)}",
            commits=[]
        )
    except Exception as e:
        return GetRecentCommitsResponse(
            success=False,
            message=f"Unexpected error: {str(e)}",
            commits=[]
        )