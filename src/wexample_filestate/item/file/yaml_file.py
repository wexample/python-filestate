from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.const.types import StructuredData

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData
    from wexample_helpers_yaml.const.types import YamlContent


class YamlFile(StructuredContentFile):
    EXTENSION_YAML: ClassVar[str] = "yaml"
    EXTENSION_YML: ClassVar[str] = "yml"

    @staticmethod
    def _get_yaml() -> YAML:
        """Return a ruamel.yaml instance configured for round-trip preservation:
        comments, anchors/aliases, key order, quote style, and custom tags
        (e.g. GitLab CI's ``!reference``) are kept intact.
        """
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.width = 4096  # avoid line-wrapping rewrites
        yaml.indent(mapping=2, sequence=4, offset=2)
        return yaml

    def dumps(self, content: StructuredData | None) -> str:
        import io

        from wexample_config.config_value.config_value import ConfigValue

        try:
            from ruamel.yaml.comments import CommentedMap, CommentedSeq
        except ImportError:
            CommentedMap = dict
            CommentedSeq = list

        def _normalize(v):
            """Unwrap ConfigValue objects to raw primitives. For ruamel
            Commented* containers, mutate in place to keep metadata intact;
            for plain dict/list, rebuild (no metadata to preserve anyway).
            """
            if isinstance(v, ConfigValue):
                return _normalize(v._get_nested_raw())
            if isinstance(v, CommentedMap):
                for k in list(v.keys()):
                    v[k] = _normalize(v[k])
                return v
            if isinstance(v, CommentedSeq):
                for i in range(len(v)):
                    v[i] = _normalize(v[i])
                return v
            if isinstance(v, dict):
                return {k: _normalize(x) for k, x in v.items()}
            if isinstance(v, list):
                return [_normalize(x) for x in v]
            return v

        normalized = _normalize(content if content is not None else {})
        buf = io.StringIO()
        self._get_yaml().dump(normalized, buf)
        return buf.getvalue()

    def loads(self, text: str, strict: bool = True) -> YamlContent:
        import io

        try:
            value = self._get_yaml().load(io.StringIO(text))
            return value if value is not None else {}
        except Exception as e:
            if strict:
                raise e
            return {}

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_YML
