from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_runner.runner.docker_runner import DockerRunner

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.item.mixin.with_runners_root_mixin import (
        WithRunnersRootMixin,
    )


class WithRunnerOptionMixin:
    # Set to True to get verbose output from the container
    _debug: bool = False
    # Set to True to force rebuild of Docker image and container
    _docker_rebuild: bool = False

    def _ensure_docker_container(self, target: TargetFileOrDirectoryType) -> None:
        image_name = self._get_docker_image_name()
        root: WithRunnersRootMixin = target.get_root()

        if self._docker_rebuild:
            existing = root.get_runner(image_name)
            if existing:
                existing.destroy()
                root.set_runner(image_name, None)

        self._get_or_create_runner(target).ensure_running()

    def _execute_in_docker(
        self, target: TargetFileOrDirectoryType, command: list[str]
    ) -> str:
        if self._is_already_rectified(target):
            return target.get_local_file().read()
        self._ensure_docker_container(target)
        result = self._get_or_create_runner(target).execute(cmd=command)
        self._mark_as_rectified(target, result.stdout)
        return result.stdout

    def _get_container_file_path(self, target: TargetFileOrDirectoryType) -> str:
        return self._get_or_create_runner(target).rebase_path(target.get_path())

    def _get_container_name(self, target: TargetFileOrDirectoryType) -> str:
        return self._get_or_create_runner(target).container_name

    @abstract_method
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name to use."""

    @abstract_method
    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Dockerfile."""

    def _get_or_create_runner(self, target: TargetFileOrDirectoryType) -> DockerRunner:
        from wexample_runner.runner.docker_runner import DockerRunner

        image_name = self._get_docker_image_name()
        root: WithRunnersRootMixin = target.get_root()
        runner = root.get_runner(image_name)

        if runner is None:
            app_root = str(root.get_path().resolve())
            user = f"{os.getuid()}:{os.getgid()}"
            runner = DockerRunner(
                image_name=image_name,
                dockerfile_path=self._get_dockerfile_path(),
                volumes={app_root: "/var/www/html"},
                workdir="/var/www/html",
                user=user,
            )
            root.set_runner(image_name, runner)

        return runner

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

    # ------------------------------------------------------------------ #
    # Batch rectification
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

    def _build_batch_cache(
        self, any_target: TargetFileOrDirectoryType
    ) -> dict[str, str]:
        """Run the tool once on temp copies of every matched file, never on the
        originals — so we can compare original vs rectified later without
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
            self._run_batch_on_paths(
                reference_target=any_target,
                paths=[temp_path for _, temp_path in temp_pairs],
            )

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

    @abstract_method
    def _run_batch_on_paths(
        self,
        reference_target: TargetFileOrDirectoryType,
        paths: list[Path],
    ) -> None:
        """Run the underlying tool once on this list of file paths (modifying
        them in place). Paths are temp copies, NOT the original project files.
        """
