from __future__ import annotations

from wexample_file.mixin.with_local_file_mixin import WithLocalFileMixin
from wexample_filestate.config_value.content_config_value import ContentConfigValue


class FileContentConfigValue(WithLocalFileMixin, ContentConfigValue):
    def __init__(self, **data) -> None:
        # Conciliate mixins.
        data["path"] = data["raw"]
        super().__init__(**data)

    def build_content(self) -> str | None:
        if self.get_path().exists():
            return self.get_local_file().read()
        return None
