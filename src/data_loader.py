"""Data loading utilities for document corpus"""

import hashlib
from pathlib import Path
from typing import Optional

import polars as pl
import pandas as pd


def scan_documents(data_dir: Path) -> pl.DataFrame:
    """
    Scan and catalog all documents in a directory.

    Args:
        data_dir: Path to directory containing documents

    Returns:
        DataFrame with file metadata (path, size, format, hash)
    """
    if not data_dir.exists():
        raise ValueError(f"Directory does not exist: {data_dir}")

    files = []
    for file_path in data_dir.rglob("*"):
        if file_path.is_file() and file_path.name != ".gitkeep":
            files.append({
                "file_path": str(file_path),
                "file_name": file_path.name,
                "extension": file_path.suffix.lower(),
                "size_bytes": file_path.stat().st_size,
                "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
                "modified_time": file_path.stat().st_mtime,
            })

    if not files:
        return pl.DataFrame()

    return pl.DataFrame(files).sort("modified_time", descending=True)


def compute_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Compute hash of a file for versioning/deduplication.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (sha256, md5)

    Returns:
        Hexadecimal hash string
    """
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_csv_lazy(file_path: Path, **kwargs) -> pl.LazyFrame:
    """
    Lazy-load large CSV files using Polars.

    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments for pl.scan_csv

    Returns:
        LazyFrame for deferred execution
    """
    return pl.scan_csv(file_path, **kwargs)


def load_text_file(file_path: Path, encoding: str = "utf-8") -> str:
    """
    Load text file content.

    Args:
        file_path: Path to text file
        encoding: File encoding

    Returns:
        File content as string
    """
    with open(file_path, encoding=encoding) as f:
        return f.read()


def check_gfs_compatibility(
    df: pl.DataFrame,
    max_size_mb: float = 100.0,
    supported_extensions: Optional[set] = None
) -> pl.DataFrame:
    """
    Check which files are compatible with GFS limits.

    Args:
        df: DataFrame from scan_documents()
        max_size_mb: Maximum file size for GFS (default 100MB)
        supported_extensions: Set of supported extensions

    Returns:
        DataFrame with 'gfs_compatible' boolean column
    """
    if supported_extensions is None:
        # GFS supported formats (subset)
        supported_extensions = {
            ".pdf", ".txt", ".md", ".csv", ".json",
            ".doc", ".docx", ".xls", ".xlsx"
        }

    return df.with_columns([
        (
            (pl.col("size_mb") <= max_size_mb) &
            (pl.col("extension").is_in(list(supported_extensions)))
        ).alias("gfs_compatible")
    ])
