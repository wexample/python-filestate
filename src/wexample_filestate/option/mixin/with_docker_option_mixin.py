from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.helpers.docker import docker_image_exists, docker_build_image, docker_container_exists, \
    docker_container_is_running, docker_start_container, docker_run_container, docker_exec

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class WithDockerOptionMixin:
    _container_name: str | None = None
    _app_root_path: str | None = None

    @abstract_method
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name to use."""
        pass

    @abstract_method
    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Dockerfile."""
        pass

    def _get_container_name(self, target: TargetFileOrDirectoryType) -> str:
        """Generate a unique container name based on app root path."""
        if self._container_name is None:
            app_root = str(target.get_root().get_path().resolve())
            # Create a hash of the path for uniqueness
            path_hash = hashlib.md5(app_root.encode()).hexdigest()[:8]
            self._container_name = f"wex-{self._get_docker_image_name()}-{path_hash}"
        return self._container_name

    def _get_container_file_path(self, target: TargetFileOrDirectoryType) -> str:
        """Get the file path as it appears inside the Docker container.

        Args:
            target: The file target

        Returns:
            The absolute path of the file inside the container (e.g., /var/www/html/src/file.php)
        """
        app_root = str(target.get_root().get_path())
        file_path = str(target.get_path())
        relative_path = file_path.replace(app_root, "").lstrip("/")
        return f"/var/www/html/{relative_path}"

    def _ensure_docker_image(self) -> None:
        image_name = self._get_docker_image_name()

        if not docker_image_exists(image_name):
            docker_build_image(image_name, self._get_dockerfile_path())

    def _ensure_docker_container(self, target: TargetFileOrDirectoryType) -> None:
        self._ensure_docker_image()

        container_name = self._get_container_name(target)
        app_root = str(target.get_root().get_path())

        if docker_container_exists(container_name):
            if not docker_container_is_running(container_name):
                docker_start_container(container_name)
        else:
            docker_run_container(
                container_name,
                self._get_docker_image_name(),
                volumes={app_root: "/var/www/html"},
            )

    def _execute_in_docker(
            self,
            target: TargetFileOrDirectoryType,
            command: list[str]
    ) -> str:
        self._ensure_docker_container(target)
        return docker_exec(self._get_container_name(target), command)
