from abc import ABC

from pydantic import BaseModel


class AbstractContentFilter(BaseModel, ABC):
    def apply_filter(self, content: str) -> str:
        pass
