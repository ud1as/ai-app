"""
Local file storage implementation.
"""
import os
from pathlib import Path
from typing import Union, Generator

from configs import config
from repository.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    """Local file storage implementation."""

    def __init__(self):
        """Initialize local storage with configured path."""
        self.storage_path = Path(config.STORAGE_LOCAL_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_full_path(self, filename: str) -> Path:
        """Get full path for a file."""
        path = self.storage_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def save(self, filename: str, data: Union[bytes, str]) -> None:
        """
        Save data to a file.

        Args:
            filename: Name of the file
            data: Data to save (bytes or string)
        """
        path = self._get_full_path(filename)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        if len(data) > config.MAX_UPLOAD_SIZE:
            raise ValueError(f"File size exceeds maximum limit of {config.MAX_UPLOAD_SIZE} bytes")
            
        with open(path, 'wb') as f:
            f.write(data)

    def load(self, filename: str) -> bytes:
        """
        Load data from a file.

        Args:
            filename: Name of the file to load

        Returns:
            File contents as bytes
        """
        path = self._get_full_path(filename)
        if not path.exists():
            raise FileNotFoundError(f"File {filename} not found")
            
        with open(path, 'rb') as f:
            return f.read()

    def exists(self, filename: str) -> bool:
        """
        Check if file exists.

        Args:
            filename: Name of the file to check

        Returns:
            True if file exists, False otherwise
        """
        return self._get_full_path(filename).exists()

    def delete(self, filename: str) -> bool:
        """
        Delete a file.

        Args:
            filename: Name of the file to delete

        Returns:
            True if file was deleted, False if file didn't exist
        """
        path = self._get_full_path(filename)
        try:
            path.unlink()
            return True
        except FileNotFoundError:
            return False


# Create global instance
storage = LocalStorage()