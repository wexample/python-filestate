import os

import pytest
from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest


class TestFileStateManager(AbstractStateManagerTest):
    def test_setup(self):
        assert self.state_manager is not None

    def test_configure_name(self):
        self.state_manager.set_value({"name": "yes"})

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with pytest.raises(InvalidOptionException):
            self.state_manager.set_value({"unexpected_option": "yes"})

    def test_configure_class_unexpected(self):
        class BadClass:
            pass

        from wexample_filestate.exception.config import BadConfigurationClassTypeException

        with pytest.raises(BadConfigurationClassTypeException):
            self.state_manager.set_value({
                "children": [
                    {
                        "class": BadClass
                    }
                ]
            })
