"""Main module for the plugin."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
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
        base, _, rest = which.name.partition('.')
        if not base and rest:
            # `.cz.json` -> `cz`
            # `.gitignore` -> `gitignore`
            base = rest if '.' not in rest else '.'.join(rest.split('.')[:-1])
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
    """cz-path commitizen class."""
    @override
    def questions(self) -> Iterable[ListQuestion | InputQuestion | ConfirmQuestion]:
        post_remove_path_prefixes = [
            x.rstrip('/')
            for x in cast('Iterable[str]', self.config.settings.get('remove_path_prefixes', (
                'src',)))
        ]
        common_path = _get_common_path()
        common_prefix = _get_common_prefix()
        choices: list[Choice] = []
        if common_path:
            for prefix in post_remove_path_prefixes:
                common_path = common_path.removeprefix(f'{prefix}/')
            common_path = common_path.lower()
            choices.append({'value': common_path, 'name': common_path, 'key': 'p'})
        if common_prefix:
            for prefix in post_remove_path_prefixes:
                common_prefix = common_prefix.removeprefix(f'{prefix}/')
            common_prefix = common_prefix.lower()
            choices.append({'value': common_prefix, 'name': common_prefix, 'key': 'r'})
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
                    'name': 'project',
                    'key': 'o'
                }, {
                    'value': '',
                    'name': '(empty)',
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
