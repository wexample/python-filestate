from typing import List, TYPE_CHECKING, Type

from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractConfigOption"]]:
        from wexample_filestate.option.class_config_option import ClassConfigOption
        from wexample_filestate.option.content_config_option import ContentConfigOption
        from wexample_filestate.option.name_pattern_config_option import NamePatternConfigOption
        from wexample_config.option.children_config_option import ChildrenConfigOption
        from wexample_filestate.option.default_content_config_option import DefaultContentConfigOption
        from wexample_filestate.option.mode_config_option import ModeConfigOption
        from wexample_filestate.option.mode_recursive_config_option import ModeRecursiveConfigOption
        from wexample_config.option.name_config_option import NameConfigOption
        from wexample_filestate.option.should_exist_config_option import ShouldExistConfigOption
        from wexample_filestate.option.type_config_option import TypeConfigOption
        from wexample_filestate.option.remove_backup_max_file_size_config_option import RemoveBackupMaxFileSizeConfigOption
        from wexample_config.config_option.name_config_option import NameConfigOption

        return [
            ChildrenConfigOption,
            ClassConfigOption,
            ContentConfigOption,
            DefaultContentConfigOption,
            ModeConfigOption,
            ModeRecursiveConfigOption,
            NameConfigOption,
            NamePatternConfigOption,
            RemoveBackupMaxFileSizeConfigOption,
            ShouldExistConfigOption,
            TypeConfigOption,
        ]
