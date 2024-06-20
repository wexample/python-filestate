class StateItemTargetMixin:
    def configure(self, config: dict):
        if "name" in config:
            self._name = config["name"]

        if "mode" in config:
            self._mode = config["mode"]
