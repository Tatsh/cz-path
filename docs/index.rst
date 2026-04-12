cz-path
=============================

.. include:: badges.rst

Commitizen plugin that prefixes commit messages with the common path or prefix of staged files.

Installation
============

Install from PyPI:

.. code-block:: shell

   pip install cz-path

The ``cz-path`` package depends on Commitizen, so installing it also provides the ``cz`` command.

Using the plugin
================

Configure Commitizen
--------------------

Set ``name`` to ``cz_path`` in your Commitizen configuration (see below). For one-off use without
editing the config file, pass ``-n cz_path`` or ``--name cz_path`` to ``cz``.

Create a commit
---------------

#. Work from the **repository root**. The plugin reads the Git index in the current directory; run
   ``cz`` there so it sees your project.

#. **Stage** the files you want in the commit with ``git add``. The plugin derives a suggested path
   prefix from the staged diff against ``HEAD``. If nothing is staged, Commitizen reports that no
   staged files were found.

#. Run Commitizen to create the commit message and commit:

   .. code-block:: shell

      cz commit

   Short form: ``cz c``.

#. Answer the prompts:

   * **Prefix** — the suggested path prefix when available, or ``project``, or ``(empty)`` for no
     prefix.
   * **Commit title** — the subject text after the prefix. The full message is
     ``<prefix>: <title>``.

Message format
--------------

Messages follow ``<prefix>: <title>``, for example ``module/component: short description of the
change``. The pattern is a prefix (which may be empty), a colon and space, and the title.

By default, ``src/`` is removed from the computed prefix. Set ``remove_path_prefixes`` to ``[]`` to
disable that, or list other path segments (such as a package directory) to strip. You do not need a
trailing ``/`` on each entry.

``pyproject.toml``
------------------

.. code-block:: toml

   [tool.commitizen]
   name = "cz_path"
   remove_path_prefixes = ["src", "module_name"]

``.cz.json``
------------

.. code-block:: json

   {
     "commitizen": {
       "name": "cz_path",
       "remove_path_prefixes": ["src", "module_name"]
     }
   }

Scenarios
---------

.. list-table::
   :header-rows: 1
   :widths: 33 33 34

   * - Staged files
     - Path prefix
     - String prefix
   * - ``src/a.c``, ``src/b.c``
     - ``src``
     - ``src/``
   * - ``src/a1.c``, ``src/a2.c``
     - ``src``
     - ``src/a``
   * - ``a.c``, ``b.c``
     - (no option)
     - (no option)

If no prefix is found among the staged files, only the choices ``project`` and empty are offered.

.. only:: html

   Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
