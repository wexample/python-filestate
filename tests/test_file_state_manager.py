import os

import pytest
from wexample_config.config_value.callback_render_config_value import (
    CallbackRenderConfigValue,
)
from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
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
        from wexample_filestate.exception.config import (
            BadConfigurationClassTypeException,
        )

        class BadClass:
            pass

        with pytest.raises(BadConfigurationClassTypeException):
            self.state_manager.set_value({"children": [{"class": BadClass}]})

    def test_configure_from_callback(self):
        def _name():
            return "yes"

        self.state_manager.set_value({"name": _name})

        assert self.state_manager.get_name() == "file_state_manager"
        assert self.state_manager.get_item_name() == "yes"

    def test_configure_from_callback_class(self):
        def _name():
            return "yow"

        self.state_manager.set_value(
            {
                "name": CallbackRenderConfigValue(raw=_name),
            }
        )

        assert self.state_manager.get_item_name() == "yow"

    def test_configure_from_file(self):
        self.state_manager.configure_from_file(
            os.path.join(self._get_test_state_manager_path(), "config-test-one.yml")
        )

    def test_dump(self):
        self.state_manager.set_value(
            {
                "children": [
                    {
                        "name": TEST_FILE_NAME_SIMPLE_TEXT,
                        "type": "file",
                    }
                ]
            }
        )

        dump = self.state_manager.dump()

        assert dump == {
            "name": "resources",
            "children": [{"name": "simple-text.txt", "type": "file"}],
        }
        assert isinstance(dump, dict)
