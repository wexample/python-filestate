from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class AbstractStateItem(BaseModel):
    path: Optional[Path] = None

    @abstractmethod
    def get_item_title(self) -> str:
        pass
