from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.helpers.docker import docker_image_exists, docker_build_image, docker_container_exists, \
    docker_container_is_running, docker_start_container, docker_run_container, docker_exec, docker_build_name_from_path
from wexample_helpers.helpers.path import path_rebase

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class WithDockerOptionMixin:
    # Set to True to force rebuild of Docker image and container
    _docker_rebuild: bool = False

    @abstract_method
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name to use."""
        pass

    @abstract_method
    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Dockerfile."""
        pass

    def _get_container_name(self, target):
        return docker_build_name_from_path(
            root_path=target.get_root().get_path(),
            image_name=self._get_docker_image_name(),
        )

    def _get_container_file_path(self, target):
        app_root = target.get_root().get_path()
        file_path = target.get_path()

        return path_rebase(
            root_src=app_root,
            path_src=file_path,
            root_dest="/var/www/html",
        )

    def _ensure_docker_image(self) -> None:
        from wexample_helpers.helpers.docker import docker_remove_image
        
        image_name = self._get_docker_image_name()

        # Force rebuild if requested
        if self._docker_rebuild and docker_image_exists(image_name):
            docker_remove_image(image_name)

        if not docker_image_exists(image_name):
            docker_build_image(image_name, self._get_dockerfile_path())

    def _ensure_docker_container(self, target: TargetFileOrDirectoryType) -> None:
        from wexample_helpers.helpers.docker import docker_stop_container, docker_remove_container
        
        self._ensure_docker_image()

        container_name = self._get_container_name(target)
        app_root = str(target.get_root().get_path())

        # Force rebuild if requested
        if self._docker_rebuild and docker_container_exists(container_name):
            if docker_container_is_running(container_name):
                docker_stop_container(container_name)
            docker_remove_container(container_name)

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
