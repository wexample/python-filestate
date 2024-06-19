from wexample_filestate.result.abstract_result import AbstractResult


class StateItemTargetMixin:
    def configure(self, config: dict):
        pass

    def build_operations(self, result: AbstractResult):
        pass
