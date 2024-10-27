import os
from typing import List, Type, Optional
from pathlib import Path

from pydantic import BaseModel
from wexample_config.classes.mixins.multiple_options_providers_mixin import MultipleOptionsProvidersMixin
from wexample_config.const.types import DictConfig
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_helpers.const.types import FileStringOrPath


class StateItemTargetMixin(MultipleOptionsProvidersMixin, BaseModel):
    base_path: FileStringOrPath
    path: Optional[Path] = None

    def __init__(self, config: DictConfig, **data):
        BaseModel.__init__(self, config=config, **data)
        MultipleOptionsProvidersMixin.__init__(self, config=config, **data)

        self.path = Path(f"{self.base_path}{config['name']}")

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]
