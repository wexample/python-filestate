from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

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
        """Build Docker image if it doesn't exist."""
        from wexample_helpers.helpers.shell import shell_run

        image_name = self._get_docker_image_name()
        
        # Check if image exists
        result = shell_run(
            cmd=["docker", "images", "-q", image_name],
            capture=True
        )

        # Build image if it doesn't exist
        if not result.stdout.strip():
            dockerfile_path = self._get_dockerfile_path()
            build_context = dockerfile_path.parent
            
            shell_run(
                cmd=[
                    "docker", "build",
                    "-t", image_name,
                    "-f", str(dockerfile_path),
                    str(build_context)
                ],
                inherit_stdio=True
            )

    def _ensure_docker_container(self, target: TargetFileOrDirectoryType) -> None:
        """Ensure Docker container is running."""
        from wexample_helpers.helpers.shell import shell_run

        # Ensure image exists
        self._ensure_docker_image()

        container_name = self._get_container_name(target)
        app_root = target.get_root().get_path()
        
        # Check if container exists
        result = shell_run(
            cmd=["docker", "ps", "-a", "-q", "-f", f"name={container_name}"],
            capture=True
        )

        if result.stdout.strip():
            # Container exists, check if it's running
            result = shell_run(
                cmd=["docker", "ps", "-q", "-f", f"name={container_name}"],
                capture=True
            )
            
            if not result.stdout.strip():
                # Container exists but not running, start it
                shell_run(
                    cmd=["docker", "start", container_name],
                    inherit_stdio=True
                )
        else:
            # Container doesn't exist, create and run it
            shell_run(
                cmd=[
                    "docker", "run",
                    "-d",
                    "--name", container_name,
                    "-v", f"{app_root}:/var/www/html",
                    self._get_docker_image_name()
                ],
                inherit_stdio=True
            )

    def _execute_in_docker(
        self, 
        target: TargetFileOrDirectoryType, 
        command: list[str]
    ) -> str:
        """Execute a command in the Docker container and return output."""
        from wexample_helpers.helpers.shell import shell_run

        self._ensure_docker_container(target)
        container_name = self._get_container_name(target)

        result = shell_run(
            cmd=["docker", "exec", container_name] + command,
            capture=True
        )

        return result.stdout
