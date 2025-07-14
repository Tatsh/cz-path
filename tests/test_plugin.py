from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pytest

if TYPE_CHECKING:
    from collections.abc import Mapping

    from commitizen.question import ListQuestion
    from pytest_mock import MockerFixture


def test_path_commitizen_questions(mocker: MockerFixture) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    mock_repo = mocker.patch('cz_path.plugin.Repo', autospec=True)
    mock_repo.return_value.index.diff.return_value = [
        mocker.Mock(a_path='src/file1.py', renamed_file=False),
        mocker.Mock(a_path='src/file2.py', renamed_file=False),
        mocker.Mock(a_path='src/subdir/file3.py',
                    renamed_file=True,
                    b_path='src/subdir/file3_new.py'),
    ]
    from cz_path.plugin import PathCommitizen
    cz = PathCommitizen(mocker.Mock(settings={}))
    questions = list(cz.questions())
    assert isinstance(questions, list)
    assert any(q['name'] == 'prefix' for q in questions)
    assert any(q['name'] == 'title' for q in questions)
    prefix_choices = next(
        cast('ListQuestion', q)['choices'] for q in questions if q['name'] == 'prefix')
    assert any(choice['value'] == 'src' for choice in prefix_choices)


def test_path_commitizen_message_no_common_prefixes(mocker: MockerFixture) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    mock_repo = mocker.patch('cz_path.plugin.Repo', autospec=True)
    mock_repo.return_value.index.diff.return_value = [
        mocker.Mock(a_path='a.py', renamed_file=False),
        mocker.Mock(a_path='b.py', renamed_file=False),
        mocker.Mock(a_path='.gitignore', renamed_file=False),
        mocker.Mock(a_path='.cz.json', renamed_file=False)
    ]
    from cz_path.plugin import PathCommitizen
    cz = PathCommitizen(mocker.Mock(settings={}))
    cz.questions()
    assert not any(q['name'] == 'Common path' for q in cz.questions())
    assert not any(q['name'] == 'Common prefix' for q in cz.questions())


def test_no_staged_files_error(mocker: MockerFixture) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    mock_repo = mocker.patch('cz_path.plugin.Repo', autospec=True)
    mock_repo.return_value.index.diff.return_value = []
    from cz_path.plugin import NoStagedFilesError, PathCommitizen
    cz = PathCommitizen(mocker.Mock(settings={}))
    with pytest.raises(NoStagedFilesError):
        cz.questions()


def test_path_commitizen_example(mocker: MockerFixture) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    from cz_path.plugin import PathCommitizen
    cz = PathCommitizen(mocker.Mock(settings={}))
    assert cz.example() == 'module/component: short description of the change'


def test_path_commitizen_schema(mocker: MockerFixture) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    from cz_path.plugin import PathCommitizen
    cz = PathCommitizen(mocker.Mock(settings={}))
    assert cz.schema() == '<prefix>: <schema>'


@pytest.mark.parametrize(
    ('answers', 'expected'),
    [
        ({
            'prefix': 'foo',
            'title': 'bar'
        }, 'foo: bar'),
        ({
            'prefix': 'foo'
        }, 'foo: (no message provided)'),
    ],
)
def test_path_commitizen_message(mocker: MockerFixture, answers: Mapping[str, Any],
                                 expected: str) -> None:
    mocker.patch('commitizen.cz.pkgutil.iter_modules', return_value=[])
    from cz_path.plugin import PathCommitizen
    cz = PathCommitizen(mocker.Mock())
    assert cz.message(answers) == expected
