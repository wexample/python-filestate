import os

import pytest
from wexample_config.config_value.callback_render_config_value import (
    CallbackRenderConfigValue,
)
from wexample_filestate.config_option.children_config_option import ChildrenConfigOption
from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest


class TestFileStateManager(AbstractStateManagerTest):
    def test_setup(self):
        assert self.state_manager is not None

    def test_configure_name(self):
        self.state_manager.configure({"name": "yes"})

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with pytest.raises(InvalidOptionException):
            self.state_manager.configure(config={"unexpected_option": "yes"})

    def test_configure_class_unexpected(self):
        from wexample_filestate.exception.config import (
            BadConfigurationClassTypeException,
        )

        class BadClass:
            pass

        with pytest.raises(BadConfigurationClassTypeException):
            self.state_manager.configure(config={"children": [{"class": BadClass}]})

    def test_configure_from_callback(self):
        def _name():
            return "yes"

        self.state_manager.configure(config={"name": _name})

        assert self.state_manager.get_key() == "file_state_manager"
        assert self.state_manager.get_item_name() == "yes"

    def test_configure_define_child(self):
        self.state_manager.allow_undefined_keys = True
        self.state_manager.configure(config=
            {
                "custom_name": ChildrenConfigOption(value=[
                    {
                        "name": TEST_FILE_NAME_SIMPLE_TEXT,
                        "type": "file",
                    }
                ], parent=self.state_manager)
            }
        )

        assert self.state_manager.dump() == {
            'name': 'resources',
            'children': [{'name': 'simple-text.txt', 'type': 'file'}]
        }

        self.state_manager.allow_undefined_keys = False

    def test_configure_from_callback_class(self):
        def _name():
            return "yow"

        self.state_manager.configure(config=
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
        self.state_manager.configure(config=
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
