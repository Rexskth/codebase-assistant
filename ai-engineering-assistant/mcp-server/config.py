"""
Configuration for the MCP Server.
Handles environment variables and settings.
"""

import os
from typing import Optional

class Config:
    """Configuration class for MCP server settings."""

    # Server settings
    HOST: str = os.getenv("MCP_HOST", "localhost")
    PORT: int = int(os.getenv("MCP_PORT", "8000"))

    # Project settings - path to the codebase to analyze
    PROJECT_PATH: str = os.getenv("PROJECT_PATH", "/Users/mac/Documents/Me/codebase-assistant")

    # Optional: API keys for future authentication
    # API_KEY: Optional[str] = os.getenv("MCP_API_KEY")

# Global config instance
config = Config()