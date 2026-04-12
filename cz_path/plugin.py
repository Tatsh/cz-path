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
        if diff.new_file or diff.renamed_file:
            if diff.b_path is None:
                msg = 'Expected b_path on new or renamed file diff'
                raise RuntimeError(msg)
            which = Path(diff.b_path)
        else:
            if diff.a_path is None:
                msg = 'Expected a_path on modified file diff'
                raise RuntimeError(msg)
            which = Path(diff.a_path)
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


class NoStagedFilesError(CzException):
    """Exception raised when there are no staged files for commit."""
    def __init__(self) -> None:
        super().__init__('No staged files found. Please stage files before committing.')


class PathCommitizen(BaseCommitizen):
    """cz-path commitizen class."""
    @override
    def questions(self) -> list[ListQuestion | InputQuestion | ConfirmQuestion]:
        post_remove_path_prefixes = [
            x.rstrip('/')
            for x in cast('Iterable[str]', self.config.settings.get('remove_path_prefixes', (
                'src',)))
        ]
        common_path = _get_common_path()
        choices: list[Choice] = []
        if common_path:
            for prefix in post_remove_path_prefixes:
                common_path = common_path.removeprefix(f'{prefix}/')
            common_path = common_path.lower()
            choices.append({'value': common_path, 'name': common_path, 'key': 'p'})
        return [{
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
        }]

    @override
    def example(self) -> str:
        return 'module/component: short description of the change'

    @override
    def schema(self) -> str:
        return '<prefix>: <schema>'

    @override
    def message(self, answers: Mapping[str, Any]) -> str:
        return f'{answers["prefix"]}: {answers.get("title", "(no message provided)")}'

    @override
    def schema_pattern(self) -> str:
        return r'^(?P<prefix>[\w\-/]*): (?P<message>.+)$'

    @override
    def info(self) -> str:
        return 'path commitizen'
