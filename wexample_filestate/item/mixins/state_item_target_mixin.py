from typing import List, Type

from pydantic import BaseModel
from wexample_config.classes.mixins.multiple_options_providers_mixin import MultipleOptionsProvidersMixin
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider


class StateItemTargetMixin(MultipleOptionsProvidersMixin, BaseModel):
    def __init__(self, **data):
        BaseModel.__init__(self, **data)
        MultipleOptionsProvidersMixin.__init__(self, **data)

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]
