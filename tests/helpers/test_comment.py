from __future__ import annotations


def test_comment_indicates_protected_keep() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("filestate: keep") is True


def test_comment_indicates_protected_ignore() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("# filestate: ignore") is True


def test_comment_indicates_protected_case_insensitive() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("FILESTATE: KEEP") is True


def test_comment_indicates_protected_false_without_tag() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("just a comment keep") is False


def test_comment_indicates_protected_false_with_tag_but_no_action() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("filestate: somethingelse") is False


def test_comment_indicates_protected_none() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected(None) is False


def test_comment_indicates_protected_empty() -> None:
    from wexample_filestate.helpers.comment import comment_indicates_protected

    assert comment_indicates_protected("") is False
