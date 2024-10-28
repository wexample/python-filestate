import os
import pytest

from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest


class TestFileStateManager(AbstractStateManagerTest):
    def test_setup(self):
        assert self.state_manager is not None

    def test_configure_name(self):
        self.state_manager.configure({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with pytest.raises(InvalidOptionException):
            self.state_manager.configure({
                "unexpected_option": "yes"
            })

    def test_configure_class_unexpected(self):
        from wexample_filestate.exception.config import BadConfigurationClassTypeException

        class BadClass:
            pass

        with pytest.raises(BadConfigurationClassTypeException):
            self.state_manager.configure({
                "children": [
                    {
                        "class": BadClass
                    }
                ]
            })

    def test_configure_from_file(self):
        self.state_manager.configure_from_file(
            os.path.join(self.get_package_resources_path(), 'config-test-one.yml')
        )
