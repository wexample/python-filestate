from pydantic import BaseModel


class AbstractResult(BaseModel):
    def configure(self, config: dict):
        self.config = config
