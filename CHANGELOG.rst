*********
Changelog
*********

This changelog mostly follows `keep a changelog <https://keepachangelog.com/en/1.0.0/>`__. Release numbering mostly
follows `Semantic Versioning <https://semver.org/spec/v2.0.0.html#semantic-versioning-200>`__.  Documentation
updates and improvements are ongoing and not listed here.

**Development**

`Contributions <https://github.com/mborsetti/webchanges/blob/main/CONTRIBUTING.rst>`__ are always welcomed, and you
can check out the `wish list <https://github.com/mborsetti/webchanges/blob/main/WISHLIST.md>`__ for inspiration.

The unreleased versions can be installed as follows (`git
<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__ needs to be installed):

.. code-block:: bash

   pip install git+https://github.com/mborsetti/webchanges.git@unreleased

Unreleased documentation is `here <https://webchanges.readthedocs.io/en/unreleased/>`__.

.. Categories used (in order):
   ⚠ Breaking Changes for changes that break existing functionality.
   Added for new features.
   Changed for changes in existing functionality.
   Deprecated for soon-to-be removed features.
   Removed for now removed features.
   Fixed for any bug fixes.
   Security in case of vulnerabilities.
   Internals for changes that don't affect users.

Version 3.2.1
=================
2021-03-08

Added
-----
* Job directive ``note``: adds a freetext note appearing in the report after the job header
* Job directive ``wait_for_navigation`` for URL jobs with ``use_browser: true`` (i.e. using Pyppeteer): wait for
  navigation to reach a URL starting with the specified one before extracting content. Useful when the URL redirects
  elsewhere before displaying content you're interested in and Pyppeteer would capture the intermediate page.
* Command line switch ``--rollback-cache TIMESTAMP``: rollback the snapshot database to a previous time, useful when
  you miss notifications; see `here <https://webchanges.readthedocs.io/en/stable/cli.html#rollback-cache>`__
* Command line switch ``--cache-engine ENGINE``: specify ``minidib`` to continue using the database structure used
  in prior versions and `urlwatch` 2.  Default ``sqlite3`` creates a smaller database due to data compression with
  `msgpack <https://msgpack.org/index.html>`__; migration from old minidb database is done automatically and the old
  database preserved for manual deletion
* Job directive ``block_elements`` for URL jobs with ``use_browser: true`` (i.e. using Pyppeteer) (⚠ ignored in Python
  < 3.7) (experimental feature): specify `resource types
  <https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/ResourceType>`__ (elements) to
  skip requesting (downloading) in order to speed up retrieval of the content; only resource types `supported by
  Chromium <https://developer.chrome.com/docs/extensions/reference/webRequest/#type-ResourceType>`__ are allowed
  (typical list includes ``stylesheet``, ``font``, ``image``, and ``media``). ⚠ On certain sites it seems to totally
  freeze execution; test before use.

Changes
-------
* A new, more efficient indexed database is used and only the most recent saved snapshot is migrated the first time you
  run this version. This has no effect on the ordinary use of the program other than reducing the number of historical
  results from ``--test-diffs`` util more snapshots are captured.  To continue using the legacy database format, launch
  with ``database-engine minidb`` and ensure that the package ``minidb`` is installed.
* If any jobs have ``use_browser: true`` (i.e. are using Pyppeteer), the maximum number of concurrent threads is set to
  the number of available CPUs instead of the `default
  <https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor>`__ to avoid
  instability due to Pyppeteer's high usage of CPU
* Default configuration now specifies the use of Chromium revisions equivalent to Chrome 89.0.4389.72 827102
  for URL jobs with ``use_browser: true`` (i.e. using Pyppeteer) to increase stability. Note: if you already have a
  configuration file and want to upgrade to this version, see `here
  <https://webchanges.readthedocs.io/en/stable/advanced.html#using-a-chromium-revision-matching-a-google-chrome-chromium-release>`__
  The Chromium revisions used now are 'linux': 843831, 'win64': 843846, 'win32': 843832, and 'macos': 843846.
* Temporarily removed code autodoc from the documentation as it's wasn't building correctly

Fixed
-----
* Specifying ``chromium_revision`` had no effect (bug introduced in version 3.1.0)
* Improved the text of the error message when ``jobs.yaml`` has a mistake in the job parameters

Internals
---------
* Removed dependency on ``minidb`` package and are now directly using Python's built-in ``sqlite3`` without additional
  layer allowing for better control and increased functionality
* Database is now smaller due to data compression with `msgpack <https://msgpack.org/index.html>`__
* An old schema database is automatically detected and the last snapshot for each job will be migrated to the new one,
  preserving the old database file for manual deletion
* No longer backing up database to `*.bak` (introduced in version 3.0.0) now that it can be rolled back
* New command line argument ``--database-engine`` allows selecting engine and accepts ``sqlite3`` (default),
  ``minidb`` (legacy compatibility, requires package by the same name) and ``textfiles`` (creates a text file of the
  latest snapshot for each job)
* When running in Python 3.7 or higher, jobs with ``use_browser: true`` (i.e. using Pyppeteer) are a bit more reliable
  as they are now launched using ``asyncio.run()``, and therefore Python takes care of managing the asyncio event loop,
  finalizing asynchronous generators, and closing the threadpool, tasks that previously were handled by custom code
* 11 percentage point increase in code testing coverage, now also testing jobs that retrieve content from the internet
  and (for Python 3.7 and up) use Pyppeteer

Known issues
------------
* ``url`` jobs with ``use_browser: true`` (i.e. using Pyppeteer) will at times display the below error message in stdout
  (terminal console). This does not affect `webchanges` as all data is downloaded, and hopefully it will be fixed in the
  future (see `Pyppeteer issue #225 <https://github.com/pyppeteer/pyppeteer/issues/225>`__):

  ``future: <Future finished exception=NetworkError('Protocol error Target.sendMessageToTarget: Target closed.')>``
  ``pyppeteer.errors.NetworkError: Protocol error Target.sendMessageToTarget: Target closed.``
  ``Future exception was never retrieved``

Version 3.1.1
=================
2021-02-08

Fixed
-----
* Documentation was failing to build at https://webchanges.readthedocs.io/

Version 3.2.1
=================
2021-02-07

Added
-----
* Can specify different values of ``chromium_revision`` (used in jobs with ``use_browser" true``, i.e. using Pyppeteer)
  based on OS by specifying keys ``linux``, ``mac``, ``win32`` and/or ``win64``
* If ``shellpipe`` filter returns an error it now shows the error text
* Show deprecation warning if running on the lowest Python version supported (mentioning the 3 years support from the
  release date of the next major version)

Fixed
-----
* ``telegram`` reporter's ``chat_id`` can be numeric (fixes # `610 <https://github.com/thp/urlwatch/issues/610>`__
  upstream by `ramelito <https://github.com/ramelito>`__)

Internals
---------
* First PyPi release with new continuous integration (CI) and continuous delivery (CD) pipeline based on `bump2version
  <https://pypi.org/project/bump2version/>`__, git tags, and `GitHub Actions <https://docs.github.com/en/actions>`__
* Moved continuous integration (CI) testing from Travis to `GitHub Actions <https://docs.github.com/en/actions>`__
* Moved linting (flake8) and documentation build testing from pytest to the `pre-commit
  <https://pre-commit.com>`__ framework
* Added automated pre-commit local testing using `tox <https://tox.readthedocs.io/en/latest/>`__
* Added continuous integration (CI) testing on macOS platform

Version 3.0.3
=============
2020-12-21

⚠ Breaking Changes
------------------
* Compatibility with `urlwatch` 2.22, including the ⚠ breaking change of removing the ability to write custom filters
  that do not take a subfilter as argument (see `here
  <https://urlwatch.readthedocs.io/en/latest/deprecated.html#filters-without-subfilters-since-2-22>`__ upstream)
* Inadvertently released as a PATCH instead of a MAJOR release as it should have been under `Semantic Versioning
  <https://semver.org/spec/v2.0.0.html#semantic-versioning-200>`__ rules given the incompatible API change upstream (see
  discussion `here <https://github.com/thp/urlwatch/pull/600#issuecomment-754525630>`__ upstream)

Added
-----
* New job subdirective ``user_visible_url`` to replace the URL in reports, useful e.g. if the watched URL is a REST
  API endpoint but you want to link to the webpage instead (# `590 <https://github.com/thp/urlwatch/pull/590>`__
  upstream by `huxiba <https://github.com/huxiba>`__)

Changed
-------
* The Markdown reporter now supports limiting the report length via the ``max_length`` parameter of the ``submit``
  method. The length limiting logic is smart in the sense that it will try trimming the details first, followed by
  omitting them completely, followed by omitting the summary. If a part of the report is omitted, a note about this is
  added to the report. (# `572 <https://github.com/thp/urlwatch/issues/572>`__ upstream by `Denis Kasak
  <https://github.com/dkasak>`__)

Fixed
-----
* Make imports thread-safe. This might increase startup times a bit, as dependencies are imported on boot instead of
  when first used, but importing in Python is not (yet) thread-safe, so we cannot import new modules from the parallel
  worker threads reliably (# `559 <https://github.com/thp/urlwatch/issues/559>`__ upstream by `Scott MacVicar
  <https://github.com/scottmac>`__)
* Write unicode-compatible YAML files

Internals
---------
* Upgraded to use of `subprocess.run <https://docs.python.org/3/library/subprocess.html#subprocess.run>`__

Version 3.0.2
=============
2020-12-06

Fixed
-----
* Logic error in reading ``EDITOR`` environment variable (# `1 <https://github.com/mborsetti/webchanges/issues/1>`__
  contributed by `MazdaFunSun <https://github.com/mazdafunsunn>`__)

Version 3.0.1
=============
2020-12-05

Added
-----
* New ``format-json`` subdirective ``sort_keys`` sets whether JSON dictionaries should be sorted (defaults to false)
* New ``webhook_markdown`` reporter for services such as Mattermost, which expects Markdown-formatted text
* Code autodoc, highlighting just how badly the code needs documentation!
* Output from ``diff_tool: wdiff`` is colorized in html reports
* Reports now show date/time of diffs when using an external ``diff_tool``

Changed and deprecated
----------------------
* Reporter ``slack`` has been renamed to ``webhook`` as it works with any webhook-enabled service such as Discord.
  Updated documentation with Discord example. The name ``slack``, while deprecated and in line to be removed in a future
  release, is still recognized.
* Improvements in report colorization code

Fixed
-----
* Fixed ``format-json`` filter from unexpectedly reordering contents of dictionaries
* Fixed documentation for ``additions_only`` and ``deletions_only`` to specify that value of true is required
* No longer creating a config directory if command line contains both ``--config`` and ``--urls``. Allow running on
  read-only systems (e.g. using redis or a database cache residing on a writeable volume)
* Deprecation warnings now use the ``DeprecationWarning`` category, which is always printed
* All filters take a subfilter (# `600 <https://github.com/thp/urlwatch/pull/600>`__ upstream by `Martin Monperrus
  <https://github.com/monperrus>`__)

Version 3.0.0
=============
2020-11-12

Milestone
---------
Initial release of `webchanges` as a reworked fork of `urlwatch` 2.21

Added
-----
Relative to `urlwatch` 2.21:

* If no job ``name`` is provided, the title of an HTML page will be used for a job name in reports
* The Python ``html2text`` package (used by the ``html2text`` filter, previously known as ``pyhtml2text``) is now
  initialized with the following purpose-optimized non-default `options
  <https://github.com/Alir3z4/html2text/blob/master/docs/usage.md#available-options>`__: unicode_snob = True,
  body_width = 0, single_line_break = True, and ignore_images = True
* The output from ``html2text`` filter is reconstructed into HTML (for html reports), preserving basic formatting
  such as bolding, italics, underlining, list bullets, etc. as well as, most importantly, rebuilding clickable links
* HTML formatting uses color (green or red) and strikethrough to mark added and deleted lines
* HTML formatting is radically more legible and useful, including long lines wrapping around
* HTML reports are now rendered correctly by email clients who override stylesheets (e.g. Gmail)
* Filter ``format-xml`` reformats (pretty-prints) XML
* ``webchanges --errors`` will run all jobs and list all errors and empty responses (after filtering)
* Browser jobs now recognize ``cookies``, ``headers``, ``http_proxy``, ``https_proxy``, and ``timeout`` sub-directives
* The revision number of Chromium browser to use can be selected with ``chromium_revision``
* Can set the user directory for the Chromium browser with ``user_data_dir``
* Chromium can be directed to ignore HTTPs errors with ``ignore_https_errors``
* Chromium can be directed as to when to consider a page loaded with ``wait_until``
* Additional command line switches can be passed to Chromium with ``switches``
* New report filters ``additions_only`` and ``deletions_only`` allow to track only content that was added (or
  deleted) from the source
* Support for Python 3.9
* Backward compatibility with `urlwatch` 2.21 (except running on Python 3.5 or using ``lynx``, which is replaced by
  internal ``html2text`` filter)

Changed and deprecated
----------------------
Relative to `urlwatch` 2.21:

* Navigation by full browser is now accomplished by specifying the ``url`` and adding the ``use_browser: true``
  directive. The `navigate` directive has been deprecated for clarity and will trigger a warning; it will be removed in
  a future release
* The name of the default program configuration file has been changed to ``config.yaml``; if at program launch
  ``urlwatch.yaml`` is found and no ``config.yaml`` exists, it is copied over for backward-compatibility.
* In Windows, the location of config files has been moved to ``%USERPROFILE%\Documents\webchanges``
  where they can be more easily edited (they are indexed there) and backed up
* The ``html2text`` filter defaults to using the Python ``html2text`` package (with optimized defaults) instead of
  ``re``
* New ``additions_only`` directive to report only added lines (useful when monitoring only new content)
* New ``deletions_only`` directive to report only deleted lines
* New ``context_line`` directive to set the number of context lines in the unified diff
* ``keyring`` Python package is no longer installed by default
* ``html2text`` and ``markdown2`` Python packages are installed by default
* Installation of Python packages required by a feature is now made easier with pip extras (e.g. ``pip install -U
  webchanges[ocr,pdf2text]``)
* The name of the default job's configuration file has been changed to ``jobs.yaml``; if at program launch ``urls.yaml``
  is found and no ``jobs.yaml`` exists, it is copied over for backward-compatibility
* The ``html2text`` filter's ``re`` method has been renamed ``strip_tags``, which is deprecated and will trigger a
  warning
* The ``grep`` filter has been renamed ``keep_lines_containing``, which is deprecated and will trigger a warning; it
  will be removed in a future release
* The ``grepi`` filter has been renamed ``delete_lines_containing``, which is deprecated and will trigger a warning; it
  will be removed in a future release
* Both the ``keep_lines_containing`` and ``delete_lines_containing`` accept ``text`` (default) in addition to ``re``
  (regular expressions)
* ``--test`` command line switch is used to test a job (formerly ``--test-filter``, deprecated and will be removed in
  a future release)
* ``--test-diff`` command line switch is used to test a jobs' diff (formerly ``--test-diff-filter``, deprecated and will
  be removed in a future release)
* ``-V`` command line switch added as an alias to ``--version``
* If a filename for ``--jobs``, ``--config`` or ``--hooks`` is supplied without a path and the file is not present in
  the current directory, `webchanges` now looks for it in the default configuration directory
* If a filename for ``--jobs`` or ``--config`` is supplied without a '.yaml' suffix, `webchanges` now looks for one with
  such a suffix
* In Windows, ``--edit`` defaults to using built-in notepad.exe if %EDITOR% or %VISUAL% are not set
* When using ``--job`` command line switch, if there's no file by that name in the specified directory will look in
  the default one before giving up.
* The use of the ``kind`` directive in ``jobs.yaml`` configuration files has been deprecated (but is, for now, still
  used internally); it will be removed in a future release
* The ``slack`` webhook reporter allows the setting of maximum report length (for, e.g., usage with Discord) using the
  ``max_message_length`` sub-directive
* Legacy lib/hooks.py file no longer supported. ``hooks.py`` needs to be in the same directory as the configuration
  files.
* The database (cache) file is backed up at every run to `*.bak`
* The mix of default and optional dependencies has been updated (see documentation) to enable "Just works"
* Dependencies are now specified as PyPi `extras
  <https://stackoverflow.com/questions/52474931/what-is-extra-in-pypi-dependency>`__ to simplify their installation
* Changed timing from `datetime <https://docs.python.org/3/library/datetime.html>`__ to `timeit.default_timer
  <https://docs.python.org/3/library/timeit.html#timeit.default_timer>`__
* Upgraded concurrent execution loop to `concurrent.futures.ThreadPoolExecutor.map
  <https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.map>`__
* Reports' elapsed time now always has at least 2 significant digits
* Expanded (only slightly) testing
* Using flake8 to check PEP-8 compliance and more
* Using coverage to check unit testing coverage
* Upgraded Travis CI to Python 3.9 from 3.9-dev and cleaned up pip installs

Removed
-------
Relative to `urlwatch` 2.21:

* The ``html2text`` filter's ``lynx`` method is no longer supported; use ``html2text`` instead
* Python 3.5 (obsoleted by 3.6 on December 23, 2016) is no longer supported

Fixed
-----
Relative to `urlwatch` 2.21:

* The ``html2text`` filter's ``html2text`` method defaults to unicode handling
* HTML href links ending with spaces are no longer broken by ``xpath`` replacing spaces with `%20`
* Initial config file no longer has directives sorted alphabetically, but are saved logically (e.g. 'enabled' is always
  the first sub-directive)
* The presence of the ``data`` directive in a job would force the method to POST preventing PUTs

Security
--------
Relative to `urlwatch` 2.21:

* None

Documentation changes
---------------------
Relative to `urlwatch` 2.21:

* Complete rewrite of the documentation

Known bugs
----------
* Documentation could be more complete
* Almost complete lack of inline docstrings in the code
