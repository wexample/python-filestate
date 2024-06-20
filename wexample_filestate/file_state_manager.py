from pydantic import BaseModel, Field


class FileStateManager(BaseModel):
    def configure(self, config: dict):
        pass
