(import 'defaults.libjsonnet') + {
  // Shared
  github_username: 'Tatsh',
  social+: {
    mastodon+: { id: '109370961877277568' },
  },
  // Project-specific
  description: 'Commitizen plugin that prefixes commit messages with the common path or prefix of staged files.',
  keywords: ['commitizen', 'commit messages', 'git', 'version control'],
  project_name: 'cz-path',
  version: '0.0.1',
  pyproject+: {
    tool+: {
      commitizen+: {
        name: 'cz_path',
        remove_path_prefixes: ['cz_path'],
      },
      poetry+: {
        dependencies+: {
          commitizen: '^4.8.3',
          gitpython: '^3.1.44',
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
  // Common
  authors: [
    {
      'family-names': 'Udvare',
      'given-names': 'Andrew',
      email: 'audvare@gmail.com',
      name: '%s %s' % [self['given-names'], self['family-names']],
    },
  ],
  github+: {
    funding+: {
      ko_fi: 'tatsh2',
      liberapay: 'tatsh2',
      patreon: 'tatsh2',
    },
  },
}
