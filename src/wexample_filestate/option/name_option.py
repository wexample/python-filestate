from __future__ import annotations

from wexample_config.config_option.name_config_option import NameConfigOption
from wexample_filestate.option.mixin.option_mixin import \
    OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameOption(OptionMixin, NameConfigOption):
    pass
