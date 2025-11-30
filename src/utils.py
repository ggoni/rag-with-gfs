"""Common utility functions"""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_api_key(env_var: str = "GOOGLE_API_KEY", env_file: str = ".env") -> str:
    """
    Load API key from environment variables.

    Args:
        env_var: Name of environment variable
        env_file: Path to .env file

    Returns:
        API key string

    Raises:
        ValueError: If API key not found
    """
    # Load from .env file if it exists
    env_path = Path(env_file)
    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(
            f"{env_var} not found. Create a .env file with: {env_var}=your_key_here"
        )

    return api_key


def format_bytes(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
