from pydantic import BaseModel

from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path


class AbstractFileStateItem(BaseModel):
    path: FileStringOrPath

    @classmethod
    def __init_model__(cls, **data):
        data['path'] = file_resolve_path(data.get('path'))
        return super().__init_model__(**data)

    def get_resolved(self):
        return self.path.resolve()
