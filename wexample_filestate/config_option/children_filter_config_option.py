from pathlib import Path
from typing import TYPE_CHECKING, List, Callable, Optional

from wexample_filestate.config_option.abstract_children_manipulator_config_option import \
    AbstractChildrenManipulationConfigOption
from wexample_filestate.config_option.name_pattern_config_option import NamePatternConfigOption
from wexample_filestate.const.disk import DiskItemType
from pydantic import Field

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ChildrenFilterConfigOption(AbstractChildrenManipulationConfigOption):
    # Optional callable used to decide whether to include an entry.
    # If provided, it takes precedence over name_pattern.
    filter: Optional[Callable[[Path], bool]] = Field(
        default=None,
        description="Use this callback to filter out the files to preserve.",
    )
    def generate_children(self) -> List["TargetFileOrDirectoryType"]:
        from wexample_filestate.helpers.config_helper import config_has_same_type_as_path
        config = self.pattern
        children = []

        name_pattern_option_name = NamePatternConfigOption.get_name()
        parent_item = self.get_parent_item()
        has_callable_filter = callable(self.filter) if self.filter is not None else False

        # Trigger generation if either a name_pattern is present or a callable filter is provided
        if config.get(name_pattern_option_name) or has_callable_filter:
            base_path: Path = parent_item.get_path()
            if base_path.exists():
                # Use the instance field `filter` when provided
                entry_filter: Optional[Callable[[Path], bool]] = self.filter if has_callable_filter else None

                for entry in base_path.iterdir():
                    entry_path: Path = entry

                    # If a specific type is requested (e.g., DIRECTORY), pre-filter by filesystem type
                    requested_type = config.get("type")
                    if requested_type == DiskItemType.DIRECTORY and not entry_path.is_dir():
                        continue
                    if requested_type == DiskItemType.FILE and not entry_path.is_file():
                        continue

                    # Inclusion decision: callback first, then name_pattern fallback
                    include = False
                    if entry_filter is not None:
                        try:
                            include = bool(entry_filter(entry_path))
                        except Exception:
                            include = False
                    else:
                        # Preserve original semantics: match on the full path string
                        include = self._path_match_patterns(str(entry_path))

                    if not include:
                        continue

                    # Validate type semantics (historical behavior)
                    if "type" in config and not config_has_same_type_as_path(config, entry_path):
                        continue

                    children.append(
                        self._create_children_from_config(
                            path=entry_path,
                            config=config,
                        )
                    )
        return children