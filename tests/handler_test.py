import contextlib
import os
import sys
import tempfile
import warnings

import pytest

from webchanges import __project_name__
from webchanges.config import BaseConfig
from webchanges.jobs import JobBase, ShellJob, UrlJob
from webchanges.main import Urlwatch
from webchanges.storage import CacheSQLite3Storage, DEFAULT_CONFIG, JobsYaml, YamlConfigStorage
from webchanges.storage_minidb import CacheMiniDBStorage
from webchanges.util import import_module_from_source

pkgname = __project_name__
root = os.path.join(os.path.dirname(__file__), f'../{pkgname}', '..')
here = os.path.dirname(__file__)


def test_required_classattrs_in_subclasses():
    for kind, subclass in JobBase.__subclasses__.items():
        assert hasattr(subclass, '__kind__')
        assert hasattr(subclass, '__required__')
        assert hasattr(subclass, '__optional__')


def test_save_load_jobs():
    jobs = [
        UrlJob(name='news', url='https://news.orf.at/'),
        ShellJob(name='list homedir', command='ls ~'),
        ShellJob(name='list proc', command='ls /proc'),
    ]

    # tempfile.NamedTemporaryFile() doesn't work on Windows
    # because the returned file object cannot be opened again
    fd, name = tempfile.mkstemp()
    JobsYaml(name).save(jobs)
    jobs2 = JobsYaml(name).load()
    os.chmod(name, 0o777)
    jobs3 = JobsYaml(name).load_secure()
    os.close(fd)
    os.remove(name)

    assert len(jobs2) == len(jobs)
    # Assert that the shell jobs have been removed due to secure loading in Linux
    if os.name == 'linux':
        assert len(jobs3) == 1


def test_load_config_yaml():
    config_file = os.path.join(here, 'data', 'config.yaml')
    if os.path.exists(config_file):
        config = YamlConfigStorage(config_file)
        assert config is not None
        assert config.config is not None
        assert config.config == DEFAULT_CONFIG
    else:
        print(f'{config_file} not found')


def test_load_jobs_yaml():
    jobs_file = os.path.join(here, 'data', 'jobs.yaml')
    if os.path.exists(jobs_file):
        assert len(JobsYaml(jobs_file).load_secure()) > 0
    else:
        warnings.warn(f'{jobs_file} not found', UserWarning)


def test_load_hooks_py():
    hooks_file = os.path.join(here, 'data', 'hooks_test.py')
    if os.path.exists(hooks_file):
        import_module_from_source('hooks', hooks_file)
    else:
        warnings.warn(f'{hooks_file} not found', UserWarning)


class ConfigForTest(BaseConfig):
    def __init__(self, config_file, urls_file, cache_file, hooks_file, verbose):
        (_, _) = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
        super().__init__(pkgname, os.path.dirname(__file__), config_file, urls_file, cache_file, hooks_file, verbose)
        self.edit = False
        self.edit_hooks = False


@contextlib.contextmanager
def teardown_func():
    try:
        yield
    finally:
        'tear down test fixtures'
        cache_file = os.path.join(here, 'data', 'cache.db')
        for filename in (cache_file, f'{cache_file}.bak', f'{cache_file}.minidb'):
            if os.path.exists(filename):
                os.remove(filename)


def test_run_watcher_minidb():
    with teardown_func():
        # jobs_file = os.path.join(root, 'share', 'examples', 'jobs-example.yaml')
        jobs_file = os.path.join(here, 'data', 'jobs.yaml')
        config_file = os.path.join(here, 'data', 'config.yaml')
        cache_file = os.path.join(here, 'data', 'cache.db')
        hooks_file = ''

        config_storage = YamlConfigStorage(config_file)
        jobs_storage = JobsYaml(jobs_file)
        cache_storage = CacheMiniDBStorage(cache_file)
        try:
            urlwatch_config = ConfigForTest(config_file, jobs_file, cache_file, hooks_file, True)

            urlwatcher = Urlwatch(urlwatch_config, config_storage, cache_storage, jobs_storage)
            urlwatcher.run_jobs()
        finally:
            cache_storage.close()


def test_run_watcher_sqlite3():
    with teardown_func():
        # jobs_file = os.path.join(root, 'share', 'examples', 'jobs-example.yaml')
        jobs_file = os.path.join(here, 'data', 'jobs.yaml')
        config_file = os.path.join(here, 'data', 'config.yaml')
        cache_file = os.path.join(here, 'data', 'cache.db')
        hooks_file = ''

        config_storage = YamlConfigStorage(config_file)
        jobs_storage = JobsYaml(jobs_file)
        cache_storage = CacheSQLite3Storage(cache_file)
        try:
            urlwatch_config = ConfigForTest(config_file, jobs_file, cache_file, hooks_file, True)

            urlwatcher = Urlwatch(urlwatch_config, config_storage, cache_storage, jobs_storage)
            urlwatcher.run_jobs()
        finally:
            cache_storage.close()


def test_unserialize_shell_job_without_kind():
    job = JobBase.unserialize({
        'name': 'hoho',
        'command': 'ls',
    })
    assert isinstance(job, ShellJob)


def test_unserialize_with_unknown_key():
    with pytest.raises(ValueError):
        JobBase.unserialize({
            'unknown_key': 123,
            'name': 'hoho',
        })


def prepare_retry_test_minidb():
    jobs_file = os.path.join(here, 'data', 'invalid-url.yaml')
    config_file = os.path.join(here, 'data', 'config.yaml')
    cache_file = os.path.join(here, 'data', 'cache.db')
    hooks_file = ''

    config_storage = YamlConfigStorage(config_file)
    cache_storage = CacheMiniDBStorage(cache_file)
    jobs_storage = JobsYaml(jobs_file)

    urlwatch_config = ConfigForTest(config_file, jobs_file, cache_file, hooks_file, True)
    urlwatcher = Urlwatch(urlwatch_config, config_storage, cache_storage, jobs_storage)

    return urlwatcher, cache_storage


def test_number_of_tries_in_cache_is_increased_minidb():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_minidb()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()
            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())

            assert tries == 2
            assert urlwatcher.report.job_states[-1].verb == 'error'
        finally:
            cache_storage.close()


def test_report_error_when_out_of_tries_minidb():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_minidb()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()
            urlwatcher.run_jobs()

            report = urlwatcher.report
            assert report.job_states[-1].verb == 'error'
        finally:
            cache_storage.close()


def test_reset_tries_to_zero_when_successful_minidb():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_minidb()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 1

            # use an url that definitely exists
            job = urlwatcher.jobs[0]
            job.url = 'file://' + os.path.join(here, 'data', 'jobs.yaml')

            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0
        finally:
            cache_storage.close()


def prepare_retry_test_sqlite3():
    jobs_file = os.path.join(here, 'data', 'invalid-url.yaml')
    config_file = os.path.join(here, 'data', 'config.yaml')
    cache_file = os.path.join(here, 'data', 'cache.db')
    hooks_file = ''

    config_storage = YamlConfigStorage(config_file)
    cache_storage = CacheSQLite3Storage(cache_file)
    jobs_storage = JobsYaml(jobs_file)

    urlwatch_config = ConfigForTest(config_file, jobs_file, cache_file, hooks_file, True)
    urlwatcher = Urlwatch(urlwatch_config, config_storage, cache_storage, jobs_storage)

    return urlwatcher, cache_storage


def test_number_of_tries_in_cache_is_increased_sqlite3():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_sqlite3()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()
            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())

            assert tries == 2
            assert urlwatcher.report.job_states[-1].verb == 'error'
        finally:
            cache_storage.close()


def test_report_error_when_out_of_tries_sqlite3():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_sqlite3()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()
            urlwatcher.run_jobs()

            report = urlwatcher.report
            assert report.job_states[-1].verb == 'error'
        finally:
            cache_storage.close()


def test_reset_tries_to_zero_when_successful_sqlite3():
    with teardown_func():
        urlwatcher, cache_storage = prepare_retry_test_sqlite3()
        try:
            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0

            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 1

            # use an url that definitely exists
            job = urlwatcher.jobs[0]
            job.url = 'file://' + os.path.join(here, 'data', 'jobs.yaml')

            urlwatcher.run_jobs()

            job = urlwatcher.jobs[0]
            old_data, timestamp, tries, etag = cache_storage.load(job.get_guid())
            assert tries == 0
        finally:
            cache_storage.close()
