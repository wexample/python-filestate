from __future__ import annotations

from pathlib import Path


def test_config_is_item_type_matches_enum() -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_is_item_type

    assert config_is_item_type({"type": DiskItemType.FILE}, DiskItemType.FILE) is True


def test_config_is_item_type_matches_enum_value() -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_is_item_type

    assert config_is_item_type({"type": "file"}, DiskItemType.FILE) is True


def test_config_is_item_type_false_on_mismatch() -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_is_item_type

    assert config_is_item_type({"type": "dir"}, DiskItemType.FILE) is False


def test_config_is_item_type_false_when_missing() -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_is_item_type

    assert config_is_item_type({}, DiskItemType.FILE) is False


def test_config_has_same_type_as_path_file(tmp_path: Path) -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_has_same_type_as_path

    file_path = tmp_path / "f.txt"
    file_path.write_text("x")
    assert (
        config_has_same_type_as_path({"type": DiskItemType.FILE}, file_path) is True
    )


def test_config_has_same_type_as_path_directory(tmp_path: Path) -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_has_same_type_as_path

    assert (
        config_has_same_type_as_path({"type": DiskItemType.DIRECTORY}, tmp_path)
        is True
    )


def test_config_has_same_type_as_path_mismatch(tmp_path: Path) -> None:
    from wexample_filestate.const.disk import DiskItemType
    from wexample_filestate.helpers.config_helper import config_has_same_type_as_path

    file_path = tmp_path / "f.txt"
    file_path.write_text("x")
    assert (
        config_has_same_type_as_path({"type": DiskItemType.DIRECTORY}, file_path)
        is False
    )
