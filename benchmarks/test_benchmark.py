"""
Benchmarks for wexample_filestate critical path.

Run with:
    pytest benchmarks/test_benchmark.py --benchmark-only

Hot paths targeted:
- FileStateManager construction + configure (option registry build)
- build_item_tree with children
- build_operations traversal (the core of app::file-state/rectify)
- find_by_name search in a built tree
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from wexample_prompt.common.io_manager import IoManager

from wexample_filestate.utils.file_state_manager import FileStateManager

# ---------------------------------------------------------------------------
# Module-level setup — shared across all read-only benchmarks
# ---------------------------------------------------------------------------

_TMP_DIR = tempfile.mkdtemp(prefix="wex_bench_filestate_")
_TMP_PATH = Path(_TMP_DIR)
_IO = IoManager()

# Create a flat set of files for children benchmarks
_FLAT_FILES = [f"file_{i}.txt" for i in range(10)]
for _fname in _FLAT_FILES:
    (_TMP_PATH / _fname).write_text(f"content of {_fname}")

# Create a nested subdirectory tree
_SUB_DIR = _TMP_PATH / "subdir"
_SUB_DIR.mkdir(exist_ok=True)
for _i in range(5):
    (_SUB_DIR / f"nested_{_i}.txt").write_text(f"nested content {_i}")

# Pre-built managers for read-only benchmarks (configure already done)
def _make_manager(config: dict) -> FileStateManager:
    return FileStateManager.create_from_path(
        io=_IO,
        path=_TMP_PATH,
        config=config,
    )

_MANAGER_EMPTY = _make_manager({})
_MANAGER_FLAT_CHILDREN = _make_manager({
    "children": [
        {"name": f, "type": "file", "should_exist": True}
        for f in _FLAT_FILES
    ]
})
_MANAGER_NESTED = _make_manager({
    "children": [
        {"name": f, "type": "file", "should_exist": True}
        for f in _FLAT_FILES
    ] + [
        {
            "name": "subdir",
            "type": "directory",
            "should_exist": True,
            "children": [
                {"name": f"nested_{i}.txt", "type": "file", "should_exist": True}
                for i in range(5)
            ],
        }
    ]
})

# ---------------------------------------------------------------------------
# FileStateManager construction — attrs init cost without configure
# ---------------------------------------------------------------------------

def test_manager_create_no_configure(benchmark):
    """Raw construction cost — attrs field init only, no option tree."""
    benchmark(
        FileStateManager.create_from_path,
        io=_IO,
        path=_TMP_PATH,
        configure=False,
    )


# ---------------------------------------------------------------------------
# configure() — option registry build + set_value + locate_source
# The registry is cached after first call per (type, providers) key.
# ---------------------------------------------------------------------------

def test_manager_configure_empty(benchmark):
    """configure({}) on a fresh manager — cold option registry build."""
    def setup():
        m = FileStateManager.create_from_path(io=_IO, path=_TMP_PATH, configure=False)
        return (m,), {}

    benchmark.pedantic(
        lambda m: m.configure({}),
        setup=setup,
        rounds=200,
    )


def test_manager_configure_flat_children(benchmark):
    """configure with 10 flat file children — tree build + 10x item init."""
    config = {
        "children": [
            {"name": f, "type": "file", "should_exist": True}
            for f in _FLAT_FILES
        ]
    }

    def setup():
        m = FileStateManager.create_from_path(io=_IO, path=_TMP_PATH, configure=False)
        return (m,), {}

    benchmark.pedantic(
        lambda m: m.configure(config),
        setup=setup,
        rounds=200,
    )


def test_manager_configure_nested(benchmark):
    """configure with 10 files + 1 dir with 5 nested files — recursive tree."""
    config = {
        "children": [
            {"name": f, "type": "file", "should_exist": True}
            for f in _FLAT_FILES
        ] + [
            {
                "name": "subdir",
                "type": "directory",
                "should_exist": True,
                "children": [
                    {"name": f"nested_{i}.txt", "type": "file", "should_exist": True}
                    for i in range(5)
                ],
            }
        ]
    }

    def setup():
        m = FileStateManager.create_from_path(io=_IO, path=_TMP_PATH, configure=False)
        return (m,), {}

    benchmark.pedantic(
        lambda m: m.configure(config),
        setup=setup,
        rounds=200,
    )


# ---------------------------------------------------------------------------
# get_allowed_options_registry — filestate adds many more options than config
# Should be instant after first call thanks to the cache in abstract_nested.
# ---------------------------------------------------------------------------

def test_options_registry_cached(benchmark):
    """Registry lookup on warm cache — should be near-zero."""
    benchmark(_MANAGER_EMPTY.get_allowed_options_registry)


# ---------------------------------------------------------------------------
# build_operations — the core of app::file-state/rectify
# Iterates the item tree, checks each option on each item.
# Uses pre-built managers so we measure traversal, not construction.
# ---------------------------------------------------------------------------

def test_build_operations_empty(benchmark):
    """build_operations on root with no children."""
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.file_state_result import FileStateResult

    def _run():
        result = FileStateResult(state_manager=_MANAGER_EMPTY)
        _MANAGER_EMPTY.build_operations(result=result, scopes=set(Scope))

    benchmark(_run)


def test_build_operations_flat_10(benchmark):
    """build_operations on a 10-file flat tree — 10x option iteration."""
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.file_state_result import FileStateResult

    def _run():
        result = FileStateResult(state_manager=_MANAGER_FLAT_CHILDREN)
        _MANAGER_FLAT_CHILDREN.build_operations(result=result, scopes=set(Scope))

    benchmark(_run)


def test_build_operations_nested(benchmark):
    """build_operations on nested tree (10 files + 1 dir + 5 nested)."""
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.file_state_result import FileStateResult

    def _run():
        result = FileStateResult(state_manager=_MANAGER_NESTED)
        _MANAGER_NESTED.build_operations(result=result, scopes=set(Scope))

    benchmark(_run)


def test_build_operations_content_scope_only(benchmark):
    """build_operations filtered to CONTENT scope — most common for rectify."""
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.file_state_result import FileStateResult

    def _run():
        result = FileStateResult(state_manager=_MANAGER_FLAT_CHILDREN)
        _MANAGER_FLAT_CHILDREN.build_operations(
            result=result, scopes={Scope.CONTENT}
        )

    benchmark(_run)


# ---------------------------------------------------------------------------
# find_by_name / find_by_type — search in a built item tree
# ---------------------------------------------------------------------------

def test_find_by_name_hit(benchmark):
    """find_by_name for a file that exists in the tree."""
    benchmark(_MANAGER_FLAT_CHILDREN.find_by_name, "file_5.txt")


def test_find_by_name_miss(benchmark):
    """find_by_name for a file that doesn't exist — full traversal."""
    benchmark(_MANAGER_FLAT_CHILDREN.find_by_name, "nonexistent.txt")


def test_find_by_name_nested(benchmark):
    """find_by_name with recursive traversal into subdir."""
    benchmark(_MANAGER_NESTED.find_by_name, "nested_4.txt")


# ---------------------------------------------------------------------------
# get_option / get_option_value — per-item config access in hot path
# ---------------------------------------------------------------------------

def test_get_option_existing(benchmark):
    """get_option for an option that is set."""
    from wexample_filestate.option.should_exist_option import ShouldExistOption

    benchmark(_MANAGER_FLAT_CHILDREN.get_option, ShouldExistOption)


def test_get_option_missing(benchmark):
    """get_option for an option that is not set — dict miss."""
    from wexample_filestate.option.content_option import ContentOption

    benchmark(_MANAGER_EMPTY.get_option, ContentOption)
