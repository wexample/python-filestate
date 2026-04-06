from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_runner.runner.docker_runner import DockerRunner


class WithRunnerOptionMixin:
    # Set to True to get verbose output from the container
    _debug: bool = False
    # Set to True to force rebuild of Docker image and container
    _docker_rebuild: bool = False
    # Cache runners by "image_name:app_root" key — shared across all instances
    _runners: ClassVar[dict[str, "DockerRunner"]] = {}

    def _get_or_create_runner(self, target: "TargetFileOrDirectoryType") -> "DockerRunner":
        from wexample_runner.runner.docker_runner import DockerRunner

        app_root = str(target.get_root().get_path().resolve())
        image_name = self._get_docker_image_name()
        cache_key = f"{image_name}:{app_root}"

        if cache_key not in self._runners:
            user = f"{os.getuid()}:{os.getgid()}"
            self._runners[cache_key] = DockerRunner(
                image_name=image_name,
                dockerfile_path=self._get_dockerfile_path(),
                volumes={app_root: "/var/www/html"},
                workdir="/var/www/html",
                user=user,
            )

        return self._runners[cache_key]

    def _ensure_docker_container(self, target: "TargetFileOrDirectoryType") -> None:
        app_root = str(target.get_root().get_path().resolve())
        image_name = self._get_docker_image_name()
        cache_key = f"{image_name}:{app_root}"

        if self._docker_rebuild and cache_key in self._runners:
            self._runners[cache_key].destroy()
            del self._runners[cache_key]

        runner = self._get_or_create_runner(target)
        runner.ensure_running()

    def _execute_in_docker(
        self, target: "TargetFileOrDirectoryType", command: list[str]
    ) -> str:
        self._ensure_docker_container(target)
        runner = self._get_or_create_runner(target)
        result = runner.execute(cmd=command)
        return result.stdout

    def _get_container_file_path(self, target: "TargetFileOrDirectoryType") -> str:
        return self._get_or_create_runner(target).rebase_path(target.get_path())

    def _get_container_name(self, target: "TargetFileOrDirectoryType") -> str:
        return self._get_or_create_runner(target).container_name

    @classmethod
    def stop_runners_for_root(cls, root_path: Path | str) -> None:
        """Stop Docker runners associated with a specific app root."""
        root_str = str(Path(root_path).resolve())
        to_remove = [key for key in cls._runners if key.endswith(f":{root_str}")]
        for key in to_remove:
            cls._runners[key].stop()
            del cls._runners[key]

    @abstract_method
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name to use."""

    @abstract_method
    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Dockerfile."""
