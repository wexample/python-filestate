from __future__ import annotations

from pathlib import Path


def test_read_dir_config_returns_parsed_yaml(tmp_path: Path) -> None:
    from wexample_filestate.helpers.dir_config import read_dir_config

    (tmp_path / ".wex.yml").write_text("key: value\n")
    assert read_dir_config(tmp_path) == {"key": "value"}


def test_read_dir_config_returns_empty_when_absent(tmp_path: Path) -> None:
    from wexample_filestate.helpers.dir_config import read_dir_config

    assert read_dir_config(tmp_path) == {}


def test_read_dir_config_returns_empty_on_empty_file(tmp_path: Path) -> None:
    from wexample_filestate.helpers.dir_config import read_dir_config

    (tmp_path / ".wex.yml").write_text("")
    assert read_dir_config(tmp_path) == {}


def test_read_dir_config_returns_empty_on_invalid_yaml(tmp_path: Path) -> None:
    from wexample_filestate.helpers.dir_config import read_dir_config

    (tmp_path / ".wex.yml").write_text("key: : : invalid")
    assert read_dir_config(tmp_path) == {}
