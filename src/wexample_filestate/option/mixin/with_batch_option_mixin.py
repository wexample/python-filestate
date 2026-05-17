from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class WithBatchOptionMixin:
    """Tool-agnostic batch rectification mechanism.

    Workflow:
      1. `prepare()` is called once before the rectification scan, builds a
         per-option cache by copying every matched file into a temp dir.
      2. The underlying tool (`_run_batch_on_paths`, abstract) runs once on
         all temp copies, modifying them in place.
      3. Rectified contents are read back into an in-memory cache.
      4. Temp dir is cleaned up.
      5. During the scan, each item's `_apply_content_change` just reads from
         the cache to decide whether a `FileWriteOperation` is needed.

    This mixin is intentionally Docker-agnostic; in-process tools (Black,
    isort, etc.) can use it directly without involving DockerRunner.
    """

    def prepare(
        self,
        root: TargetFileOrDirectoryType,
        scopes,
        filter_paths: list[str] | None = None,
    ) -> None:
        """Eagerly build the batch cache and surface the tool's output."""
        key = self._get_batch_cache_key()
        if root.get_batch_cache(key) is not None:
            return  # Already prepared

        items = self._collect_batch_targets(root)
        if not items:
            return

        root.io.log(f"[prepare] {key}: running on {len(items)} file(s)…")
        cache = self._build_batch_cache(root)
        root.set_batch_cache(key, cache)
        root.io.log(f"[prepare] {key}: done ({len(cache)} files cached).")

    def _build_batch_cache(
        self, any_target: TargetFileOrDirectoryType
    ) -> dict[str, str]:
        """Run the tool once on temp copies of every matched file, never on
        the originals — so we can compare original vs rectified later without
        polluting the working tree.
        """
        import shutil
        import uuid

        items = self._collect_batch_targets(any_target.get_root())
        if not items:
            return {}

        root_path = any_target.get_root().get_path().resolve()
        temp_root = (
            root_path
            / ".wex"
            / "tmp"
            / "batch"
            / self._get_batch_cache_key()
            / uuid.uuid4().hex
        )
        temp_root.mkdir(parents=True, exist_ok=True)

        temp_pairs: list[tuple[TargetFileOrDirectoryType, Path]] = []
        for item in items:
            rel = item.get_path().resolve().relative_to(root_path)
            temp_path = temp_root / rel
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item.get_path(), temp_path)
            temp_pairs.append((item, temp_path))

        try:
            result = self._run_batch_on_paths(
                reference_target=any_target,
                paths=[temp_path for _, temp_path in temp_pairs],
            )
            self._surface_batch_result(any_target.get_root(), result)

            cache: dict[str, str] = {}
            for item, temp_path in temp_pairs:
                new_content = temp_path.read_text()
                cache[str(item.get_path())] = new_content
                self._mark_as_rectified(item, new_content)
            return cache
        finally:
            shutil.rmtree(temp_root, ignore_errors=True)

    def _collect_batch_targets(self, root) -> list[TargetFileOrDirectoryType]:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory

        items: list[TargetFileOrDirectoryType] = []
        option_cls = type(self)

        def collect(item: TargetFileOrDirectoryType) -> None:
            if not item.get_path().is_file():
                return
            if item.get_option_recursive(option_cls) is None:
                return
            if self._is_already_rectified(item):
                return
            items.append(item)

        if isinstance(root, ItemTargetDirectory):
            root.for_each_child_recursive(collect)
        return items

    # ------------------------------------------------------------------ #
    # Batch cache
    # ------------------------------------------------------------------ #
    def _get_batch_cache_key(self) -> str:
        return type(self).__name__

    def _get_or_build_batch_cache(
        self, target: TargetFileOrDirectoryType
    ) -> dict[str, str]:
        root = target.get_root()
        key = self._get_batch_cache_key()
        cache = root.get_batch_cache(key)
        if cache is None:
            cache = self._build_batch_cache(target)
            root.set_batch_cache(key, cache)
        return cache

    # ------------------------------------------------------------------ #
    # Rectification hash tracking
    # ------------------------------------------------------------------ #
    def _hash(self, content: str) -> str:
        import hashlib

        return hashlib.md5(content.encode()).hexdigest()

    def _is_already_rectified(self, target: TargetFileOrDirectoryType) -> bool:
        key = str(target.get_path())
        current_hash = self._hash(target.get_local_file().read())
        return target.get_root().get_rectify_hash(key) == current_hash

    def _mark_as_rectified(
        self, target: TargetFileOrDirectoryType, rectified_content: str
    ) -> None:
        key = str(target.get_path())
        target.get_root().set_rectify_hash(key, self._hash(rectified_content))

    @abstract_method
    def _run_batch_on_paths(
        self,
        reference_target: TargetFileOrDirectoryType,
        paths: list[Path],
    ) -> None:
        """Run the underlying tool once on this list of file paths (modifying
        them in place). Paths are temp copies, NOT the original project files.
        Return the runner result if any, so its stdout/stderr can be surfaced;
        return None for in-process tools that don't produce one.
        """

    def _surface_batch_result(self, root, result) -> None:
        """Display the tool's stdout/stderr so silent failures are visible.
        Raise FileStateBatchToolException on non-zero exit code.
        In-process tools that don't produce a result can return None — this
        method just no-ops.
        """
        if result is None:
            return
        stdout = (getattr(result, "stdout", "") or "").strip()
        stderr = (getattr(result, "stderr", "") or "").strip()
        exit_code = getattr(result, "exit_code", 0)

        if stdout:
            root.io.log(stdout)
        if stderr:
            io_fn = root.io.warning if exit_code == 0 else root.io.error
            io_fn(stderr)

        if exit_code != 0:
            from wexample_filestate.exception.file_state_batch_tool_exception import (
                FileStateBatchToolException,
            )

            raise FileStateBatchToolException(
                message=(
                    f"Batch tool '{self._get_batch_cache_key()}' exited with "
                    f"code {exit_code}. See output above."
                ),
                data={"exit_code": exit_code},
            )
