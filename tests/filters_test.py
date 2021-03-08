"""tests filters based on a set of patterns"""

import logging
import os
import sys

import pytest
import yaml

from webchanges.filters import FilterBase

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/31469707/
if sys.version_info[0:2] == (3, 6) and os.name == 'nt':
    import _locale

    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


TESTDATA = [
    # Legacy string-style filter definition conversion  DEPRECATED
    # ('keep_lines_containing', [('keep_lines_containing', {})]),
    # ('keep_lines_containing:foo', [('keep_lines_containing', {'text': 'foo'})]),
    # ('beautify,keep_lines_containing:foo,html2text', [('beautify', {}), ('keep_lines_containing', {'text': 'foo'}),
    #                                                   ('html2text', {})]),
    # ('re.sub:.*', [('re.sub', {'pattern': '.*'})]),
    # ('re.sub', [('re.sub', {})]),

    # New dict-style filter definition normalization/mapping
    ([{'keep_lines_containing': None}], [('keep_lines_containing', {})]),
    ([{'keep_lines_containing': {'re': 'bla'}}], [('keep_lines_containing', {'re': 'bla'})]),
    ([{'reverse': '\n\n'}], [('reverse', {'separator': '\n\n'})]),
    (['html2text', {'keep_lines_containing': 'Current.version'}, 'strip'], [
        ('html2text', {}),
        ('keep_lines_containing', {'text': 'Current.version'}),
        ('strip', {}),
    ]),
    ([{'css': 'body'}], [('css', {'selector': 'body'})]),
    ([{'html2text': {'method': 'bs4', 'parser': 'html5lib'}}], [
        ('html2text', {'method': 'bs4', 'parser': 'html5lib'}),
    ]),
]


@pytest.mark.parametrize('input, output', TESTDATA)
def test_normalize_filter_list(input, output):
    assert list(FilterBase.normalize_filter_list(input)) == output


FILTER_TESTS = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), 'data/filter_tests.yaml'), 'r'))


@pytest.mark.parametrize('test_name, test_data', FILTER_TESTS.items())
def test_filters(test_name, test_data):
    filter = test_data['filter']
    data = test_data['data']
    expected_result = test_data['expected_result']

    result = data
    for filter_kind, subfilter in FilterBase.normalize_filter_list(filter):
        logger.info(f'filter kind: {filter_kind}, subfilter: {subfilter}')
        filtercls = FilterBase.__subclasses__.get(filter_kind)
        if filtercls is None:
            raise ValueError('Unknown filter kind: {filter_kind}:{subfilter}')
        result = filtercls(None, None).filter(result, subfilter)

    logger.debug('Expected result:\n%s', expected_result)
    logger.debug('Actual result:\n%s', result)
    assert result == expected_result.rstrip()


def test_invalid_filter_name_raises_valueerror():
    with pytest.raises(ValueError):
        list(FilterBase.normalize_filter_list(['afilternamethatdoesnotexist']))


def test_providing_subfilter_to_filter_without_subfilter_raises_valueerror():
    with pytest.raises(ValueError):
        list(FilterBase.normalize_filter_list([{'beautify': {'asubfilterthatdoesnotexist': True}}]))


def test_providing_unknown_subfilter_raises_valueerror():
    with pytest.raises(ValueError):
        list(FilterBase.normalize_filter_list([{'keep_lines_containing': {'re': 'Price: .*',
                                                                          'anothersubfilter': '42'}}]))


def test_shellpipe_inherits_environment_but_does_not_modify_it():
    # https://github.com/thp/urlwatch/issues/541

    if os.name != 'nt':
        # Set a specific value to check it doesn't overwrite the current env
        os.environ['URLWATCH_JOB_NAME'] = 'should-not-be-overwritten'

        # See if the shellpipe process can use a variable from the outside
        os.environ['INHERITED_FROM'] = 'parent-process'
        filtercls = FilterBase.__subclasses__.get('shellpipe')
        result = filtercls(None, None).filter('input-string', {'command': 'echo "$INHERITED_FROM/$URLWATCH_JOB_NAME"'})
        # Check that the inherited value and the job name is set properly
        assert result == 'parent-process/\n'

        # Check that outside the variable wasn't overwritten by the filter
        assert os.environ['URLWATCH_JOB_NAME'] == 'should-not-be-overwritten'
