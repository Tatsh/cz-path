"""Main module for the plugin."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any
import os.path

from commitizen.cz.base import BaseCommitizen
from commitizen.cz.exceptions import CzException
from git import Diff, Repo
from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from commitizen.question import Choice, ConfirmQuestion, InputQuestion, ListQuestion

__all__ = ('PathCommitizen',)


def _parse_diffs(diffs: Iterable[Diff]) -> Iterable[str]:
    for diff in diffs:
        assert diff.a_path is not None
        which = Path(diff.a_path)
        if diff.renamed_file:
            assert diff.b_path is not None
            which = Path(diff.b_path)
        base, _, _ = which.name.partition('.')
        yield str(which.with_name(base))


def _get_staged_files() -> Iterable[str]:
    staged_files = Repo('.').index.diff('HEAD')
    if not staged_files:
        raise NoStagedFilesError
    return _parse_diffs(staged_files)


def _get_common_path() -> str:
    return os.path.commonpath(_get_staged_files())


def _get_common_prefix() -> str:
    return os.path.commonprefix(list(_get_staged_files()))


class NoStagedFilesError(CzException):
    """Exception raised when there are no staged files for commit."""
    def __init__(self) -> None:
        super().__init__('No staged files found. Please stage files before committing.')


class PathCommitizen(BaseCommitizen):
    """cz-section commitizen class."""
    @override
    def questions(self) -> Iterable[ListQuestion | InputQuestion | ConfirmQuestion]:
        common_path = _get_common_path()
        common_prefix = _get_common_prefix()
        choices: list[Choice] = []
        if common_path:
            choices.append({'value': common_path, 'name': 'Common path', 'key': 'p'})
        if common_prefix:
            choices.append({'value': common_prefix, 'name': 'Common prefix', 'key': 'r'})
        return ({
            'type':
                'list',
            'name':
                'prefix',
            'message':
                'Prefix:',
            'choices': [
                *choices, {
                    'value': 'project',
                    'name': 'Project root',
                    'key': 'o'
                }, {
                    'value': '',
                    'name': 'Nothing',
                    'key': 'n'
                }
            ]
        }, {
            'type': 'input',
            'name': 'title',
            'message': 'Commit title:'
        })

    @override
    def example(self) -> str:
        return 'module/component: short description of the change'

    @override
    def schema(self) -> str:
        return '<prefix>: <schema>'

    @override
    def message(self, answers: Mapping[str, Any]) -> str:
        return f'{answers["prefix"]}: {answers.get("title", "(no message provided)")}'
