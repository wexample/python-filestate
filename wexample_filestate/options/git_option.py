from typing import Type
from types import UnionType

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.options.abstract_option import AbstractOption
from wexample_filestate.options.should_exist_option import ShouldExistOption


class GitOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "git"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return dict | bool

    def should_have_git(self) -> bool:
        return self.value_should_have_git(self.value)

    @staticmethod
    def value_should_have_git(value) -> bool:
        return (value is True) or isinstance(value, dict)

    @classmethod
    def resolve_config(cls, config: StateItemConfig) -> StateItemConfig:
        if "git" in config and cls.value_should_have_git(config["git"]):
            config[ShouldExistOption.get_name()] = True
        return config
