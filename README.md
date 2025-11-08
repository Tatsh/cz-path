# cz-path

[![Python versions](https://img.shields.io/pypi/pyversions/cz-path.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/cz-path)](https://pypi.org/project/cz-path/)
[![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/cz-path)](https://github.com/Tatsh/cz-path/tags)
[![License](https://img.shields.io/github/license/Tatsh/cz-path)](https://github.com/Tatsh/cz-path/blob/master/LICENSE.txt)
[![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/cz-path/v0.0.3/master)](https://github.com/Tatsh/cz-path/compare/v0.0.3...master)
[![CodeQL](https://github.com/Tatsh/cz-path/actions/workflows/codeql.yml/badge.svg)](https://github.com/Tatsh/cz-path/actions/workflows/codeql.yml)
[![QA](https://github.com/Tatsh/cz-path/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/cz-path/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/cz-path/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/cz-path/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/cz-path/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/cz-path?branch=master)
[![Documentation Status](https://readthedocs.org/projects/cz-path/badge/?version=latest)](https://cz-path.readthedocs.org/?badge=latest)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)
[![pytest](https://img.shields.io/badge/pytest-zz?logo=Pytest&labelColor=black&color=black)](https://docs.pytest.org/en/stable/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Downloads](https://static.pepy.tech/badge/cz-path/month)](https://pepy.tech/project/cz-path)
[![Stargazers](https://img.shields.io/github/stars/Tatsh/cz-path?logo=github&style=flat)](https://github.com/Tatsh/cz-path/stargazers)

[![@Tatsh](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%2F%3Factor%3Ddid%3Aplc%3Auq42idtvuccnmtl57nsucz72%26query%3D%24.followersCount%26style%3Dsocial%26logo%3Dbluesky%26label%3DFollow%2520%40Tatsh&query=%24.followersCount&style=social&logo=bluesky&label=Follow%20%40Tatsh)](https://bsky.app/profile/Tatsh.bsky.social)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/109370961877277568?domain=hostux.social&style=social)](https://hostux.social/@Tatsh)

Commitizen plugin that prefixes commit messages with the common path or prefix of staged files.

## Installation

### Poetry

Example with `dev` group:

```shell
poetry add -G dev cz-path
```

### Pip

```shell
pip install cz-path
```

## Usage

Pass `-n cz_path` to `cz` or add it to your configuration file.

By default, `src/` will be removed from any determined prefix. This can be customised by setting
`remove_path_prefixes` to `[]`. You also may want to add other locations such as a module name.
Adding `/` is not required.

### `pyproject.toml`

```toml
[tool.commitizen]
name = "cz_path"
remove_path_prefixes = ["src", "module_name"]
```

### `.cz.json`

```json
{
  "commitizen": {
    "name": "cz_path",
    "remove_path_prefixes": ["src", "module_name"]
  }
}
```

### Scenarios

| Staged files           | Path prefix | String prefix |
| ---------------------- | ----------- | ------------- |
| `src/a.c`, `src/b.c`   | `src`       | `src/`        |
| `src/a1.c`, `src/a2.c` | `src`       | `src/a`       |
| `a.c`, `b.c`           | (no option) | (no option)   |

If no prefix is found amongst the staged files, only the choices `project` and empty will be given.
