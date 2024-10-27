from __future__ import annotations
from abc import ABC
from pydantic import BaseModel


class AbstractOperation(BaseModel, ABC):
    pass
