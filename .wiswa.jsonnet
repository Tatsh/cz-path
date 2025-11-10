local utils = import 'utils.libjsonnet';

{
  description: 'Commitizen plugin that prefixes commit messages with the common path or prefix of staged files.',
  keywords: ['commitizen', 'commit messages', 'git', 'version control'],
  project_name: 'cz-path',
  version: '0.0.4',
  pyproject+: {
    tool+: {
      commitizen+: {
        name: 'cz_path',
        remove_path_prefixes: ['cz_path'],
      },
      poetry+: {
        dependencies+: {
          commitizen: utils.latestPypiPackageVersionCaret('commitizen'),
          gitpython: utils.latestPypiPackageVersionCaret('gitpython'),
        },
        plugins: {
          'commitizen.plugin': { cz_path: 'cz_path.plugin:PathCommitizen' },
        },
      },
    },
  },
  copilot: {
    intro: 'cz-path is a plugin for Commitizen that gives options to prefix commit messages with a common path or common prefix of staged files.',
  },
}
