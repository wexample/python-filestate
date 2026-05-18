from __future__ import annotations

from pathlib import Path

from wexample_filestate.const.globals import DIR_CONFIG_FILENAME


def read_dir_config(path: Path) -> dict:
    """Read the .wex.yml local config from a directory. Returns empty dict if absent or invalid."""
    import yaml

    config_path = path / DIR_CONFIG_FILENAME
    if not config_path.is_file():
        return {}

    try:
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}
