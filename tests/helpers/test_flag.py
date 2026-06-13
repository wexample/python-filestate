from __future__ import annotations


def test_flag_exists_simple_marker() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    assert flag_exists("my-flag", "# filestate: my-flag") is True


def test_flag_exists_with_leading_whitespace_and_spacing() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    assert flag_exists("my-flag", "    #   filestate:   my-flag   ") is True


def test_flag_exists_within_multiline_text() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    text = "line one\n# filestate: keep\nline three"
    assert flag_exists("keep", text) is True


def test_flag_exists_false_when_absent() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    assert flag_exists("missing", "# filestate: other") is False


def test_flag_exists_is_case_sensitive_for_flag() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    assert flag_exists("Keep", "# filestate: keep") is False


def test_flag_exists_word_boundary() -> None:
    from wexample_filestate.helpers.flag import flag_exists

    assert flag_exists("keep", "# filestate: keepsake") is False
