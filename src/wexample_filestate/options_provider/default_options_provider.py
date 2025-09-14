from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        from wexample_config.config_option.name_config_option import NameConfigOption
        from wexample_filestate.option.active_option import (
            ActiveConfigOption,
        )
        from wexample_filestate.option.children_option import (
            ChildrenConfigOption,
        )
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryConfigOption,
        )
        from wexample_filestate.option.class_option import (
            ClassConfigOption,
        )
        from wexample_filestate.option.content_option import (
            ContentConfigOption,
        )
        from wexample_filestate.option.content_options_option import (
            ContentOptionsConfigOption,
        )
        from wexample_filestate.option.default_content_option import (
            DefaultContentConfigOption,
        )
        from wexample_filestate.option.mode_option import ModeConfigOption
        from wexample_filestate.option.mode_recursive_option import (
            ModeRecursiveConfigOption,
        )
        from wexample_filestate.option.name_pattern_option import (
            NamePatternConfigOption,
        )
        from wexample_filestate.option.remove_backup_max_file_size_option import (
            RemoveBackupMaxFileSizeConfigOption,
        )
        from wexample_filestate.option.shortcut_option import (
            ShortcutConfigOption,
        )
        from wexample_filestate.option.should_contain_lines_option import (
            ShouldContainLinesConfigOption,
        )
        from wexample_filestate.option.should_exist_option import (
            ShouldExistConfigOption,
        )
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionConfigOption,
        )
        from wexample_filestate.option.should_not_contain_lines_option import (
            ShouldNotContainLinesConfigOption,
        )
        from wexample_filestate.option.text_filter_option import (
            TextFilterConfigOption,
        )
        from wexample_filestate.option.type_option import TypeConfigOption
        from wexample_filestate.option.yaml_filter_option import (
            YamlFilterConfigOption,
        )

        return [
            ActiveConfigOption,
            ChildrenConfigOption,
            ChildrenFileFactoryConfigOption,
            ClassConfigOption,
            ContentConfigOption,
            ContentOptionsConfigOption,
            DefaultContentConfigOption,
            ModeConfigOption,
            ModeRecursiveConfigOption,
            NameConfigOption,
            NamePatternConfigOption,
            RemoveBackupMaxFileSizeConfigOption,
            ShortcutConfigOption,
            ShouldContainLinesConfigOption,
            ShouldNotContainLinesConfigOption,
            ShouldExistConfigOption,
            ShouldHaveExtensionConfigOption,
            TextFilterConfigOption,
            TypeConfigOption,
            YamlFilterConfigOption,
        ]
