from __future__ import annotations

from pydantic import BaseModel


class FileStateItemDirectoryTarget(BaseModel):
    @classmethod
    def create_from_path(cls):
        return cls()
