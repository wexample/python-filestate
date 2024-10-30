from typing import TYPE_CHECKING, List, Type

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )


class StateItemTargetMixin(AbstractNestedConfigOption):

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        return [
            DefaultOptionsProvider,
        ]
