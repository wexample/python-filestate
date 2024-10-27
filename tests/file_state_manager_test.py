from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest


class TestFileStateManagerTest(AbstractStateManagerTest):
    def test_setup(self):
        self.assertIsNotNone(
            self.state_manager
        )

    def test_configure_name(self):
        self.state_manager.configure({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with self.assertRaises(InvalidOptionException):
            self.state_manager.configure({
                "unexpected_option": "yes"
            })
