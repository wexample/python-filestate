from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


# Jekyll-style fenced YAML front matter.
_FRONT_MATTER_FENCE = "---"


@base_class
class MarkdownFile(StructuredContentFile):
    """A Markdown file optionally prefixed with a fenced YAML front matter:

        ---
        key: value
        ---

        # Heading

        Body content…

    The parsed representation is `{"front": <dict>, "body": <str>}`. Files
    without a front matter parse as `{"front": {}, "body": <full text>}`.
    Round-trip preserves ruamel.yaml metadata on the front matter (comments,
    key order) and the body verbatim.
    """

    EXTENSION_MARKDOWN: ClassVar[str] = "md"

    def dumps(self, content: Any | None) -> str:
        from io import StringIO

        from wexample_config.config_value.config_value import ConfigValue

        if content is None:
            content = {"front": {}, "body": ""}
        if isinstance(content, ConfigValue):
            content = content._get_nested_raw()
        if (
            not isinstance(content, dict)
            or "front" not in content
            or "body" not in content
        ):
            raise ValueError(
                "MarkdownFile.dumps expects a dict with keys 'front' and 'body'."
            )

        front = content["front"] or {}
        body = content["body"] or ""

        if not front:
            return body if body.endswith("\n") or body == "" else f"{body}\n"

        from wexample_filestate.item.file.yaml_file import YamlFile

        yaml = YamlFile._get_yaml()
        buf = StringIO()
        yaml.dump(front, buf)
        front_text = buf.getvalue().rstrip("\n")

        body_text = body.lstrip("\n")
        if body_text and not body_text.endswith("\n"):
            body_text += "\n"

        return (
            f"{_FRONT_MATTER_FENCE}\n"
            f"{front_text}\n"
            f"{_FRONT_MATTER_FENCE}\n\n"
            f"{body_text}"
        )

    def loads(self, text: str, strict: bool = True) -> dict[str, Any]:
        from io import StringIO

        if not text.startswith(_FRONT_MATTER_FENCE):
            return {"front": {}, "body": text}

        # Locate the closing fence (must start its own line).
        search_from = len(_FRONT_MATTER_FENCE)
        end_idx = text.find(f"\n{_FRONT_MATTER_FENCE}", search_from)
        if end_idx == -1:
            # Malformed: opening fence but no close. Treat as body.
            return {"front": {}, "body": text}

        front_raw = text[search_from + 1 : end_idx]
        body = text[end_idx + len(_FRONT_MATTER_FENCE) + 1 :].lstrip("\n")

        from wexample_filestate.item.file.yaml_file import YamlFile

        try:
            front = YamlFile._get_yaml().load(StringIO(front_raw))
            if front is None:
                front = {}
        except Exception as e:
            if strict:
                raise e
            front = {}

        return {"front": front, "body": body}

    def read_body(self, reload: bool = False) -> str:
        return self.read_parsed(reload=reload).get("body", "")

    def read_front_matter(self, reload: bool = False) -> NestedConfigValue:
        from copy import deepcopy

        from wexample_config.config_value.nested_config_value import NestedConfigValue

        front = self.read_parsed(reload=reload).get("front") or {}
        return NestedConfigValue(raw=deepcopy(front))

    def write_content(
        self,
        front: dict[str, Any] | None = None,
        body: str | None = None,
    ) -> None:
        current = (
            self._parsed_cache
            if self._parsed_cache is not None
            else {"front": {}, "body": ""}
        )
        new_front = front if front is not None else current.get("front", {})
        new_body = body if body is not None else current.get("body", "")
        self.write_parsed({"front": new_front, "body": new_body})

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_MARKDOWN
