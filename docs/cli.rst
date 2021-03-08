.. _command_line:

=====================
Command line switches
=====================

.. code-block::

  optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -v, --verbose         show debug output

  override file defaults:
    --jobs FILE, --urls FILE
                          read job list (URLs) from FILE
    --config FILE         read configuration from FILE
    --hooks FILE          use FILE as hooks.py module
    --cache FILE          use FILE as cache database, alternatively can accept a redis URI

  job management:
    --list                list jobs
    --test JOB, --test-filter JOB
                          test filter output of job by location or index
    --test-diff JOB, --test-diff-filter JOB
                          test diff filter output of job by location or index (needs at least 2
                          snapshots)
    --errors              list jobs with errors or no data captured
    --add JOB             add job (key1=value1,key2=value2,...) (obsolete; use --edit)
    --delete JOB          delete job by location or index (obsolete; use --edit)

  reporters:
    --test-reporter REPORTER
                          send a test notification
    --smtp-login          check SMTP login
    --telegram-chats      list telegram chats the bot is joined to
    --xmpp-login          enter password for XMPP (store in keyring)

  launch editor ($EDITOR/$VISUAL):
    --edit                edit URL/job list
    --edit-config         edit configuration file
    --edit-hooks          edit hooks script

  miscellaneous:
    --gc-cache            garbage collect the cache database by removing old snapshots plus all data
                          of old jobs now deleted
    --clean-cache         remove old snapshots from the cache database
    --rollback-cache TIMESTAMP
                          delete recent snapshots > timestamp; backup the database before using!
    --database-engine {sqlite3,minidb,textfiles}
                          database engine to use (default: sqlite3)
    --features            list supported job types, filters and reporters


.. _rollback-cache:

Roll back the snapshot database
-------------------------------

You can roll back the database to an earlier time by running `webchanges` with the ``--rollback-cache`` switch followed
by a `Unix timestamp <https://en.wikipedia.org/wiki/Unix_time>`__ indicating the point in time you want to go back to.
Useful when you missed notifications or they got lost: roll back the database to the time of the last good report, then
run `webchanges` again to get a new report with the differences since that time.

You can find multiple sites that calculate Unix time for you, such as https://www.unixtimestamp.com/

**WARNING: all snapshots captured after the timestamp value are permanently deleted. This is irreversible.**  Back up
the database before doing a rollback in case of a mistake (or fat-finger).

This feature only works with the default ``sqlite3`` database engine.


.. _database-engine:

Select a database engine
-------------------------

The requirement for the ``minidb`` database engine has been removed in version 3.2 and the database system has migrated
to one that relies on the built-in ``sqlite3``, is more efficient due to indexing, creates smaller files due to data
compression with `msgpack <https://msgpack.org/index.html>`__ and provides additional functionality. Migration from the
old-style database is done automatically and the old file is preserved for manual deletion.

To continue using the minidb-based database structure used in prior versions and in `urlwatch` 2, launch `webchanges`
with the command line switch ``--cache-engine minidb``. The ``minidib`` package must be installed for this to work.

To have the latest snapshot of each job saved as a separate text file instead of as a record in a database, use
``--cache-engine textfiles``.
