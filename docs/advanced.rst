.. _advanced_topics:

==============
Usage examples
==============

Checking different sources at different intervals
-------------------------------------------------
You can divide your jobs into multiple job lists depending on how often you want to check.  For example, you can have
a ``daily.yaml`` job list for daily jobs, and a ``weekly.yaml`` for weekly ones.  You then set up the scheduler to
run :program:`webchanges`, defining which job list to use, at different intervals.  For example in Linux using cron::

  0 0 * * * webchanges --jobs daily.yaml
  0 0 0 * * webchanges --jobs weekly.yaml


Getting reports via different channels for different sources
------------------------------------------------------------
Job-specific alerts (reports) is not a functionality of :program:`webchanges`, but you can work around this by creating
multiple configurations and job lists, and run :program:`webchanges` multiple times specifying ``--jobs`` and
``--config``.

For example, you can create two configuration files, e.g. ``config-slack.yaml`` and ``config-email.yaml`` (the
first set for slack reporting and the second for email reporting) and two job lists, e.g. ``slack.yaml`` and
``email.yaml`` (the first containing jobs you want to be notified of via slack, the second for jobs you want to be
notified of via email).  You can then run :program:`webchanges` similarly to the below example (taken from Linux
crontab)::

  00 00 * * * webchanges --jobs slack.yaml --config config-slack.yaml
  05 00 * * * webchanges --jobs email.yaml --config config-email.yaml


.. _timeout:

Changing the default timeout
----------------------------
By default, url jobs timeout after 60 seconds. If you want a different timeout period, use the ``timeout`` directive to
specify it in number of seconds, or set it to 0 to never timeout.

.. code-block:: yaml

   url: https://example.com/
   timeout: 300


.. _headers:

Setting default headers
-----------------------
It is possible to set default headers for HTTP requests by entering them in ``config.yaml`` under ``job_defaults``, as
per the example below. If a ``headers`` key is also found in a job, for that job the headers will be merged
(case-insensitively) one by one with any conflict resolved in favor of the header specified in the job.

.. code-block:: yaml

   job_defaults:
     all:
       headers:
         Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
         Accept-Language: en-US,en
         Device-Memory: '0.25'
         DNT: '1'
         Downlink: '0.384'
         DPR: '1.5'
         ECT: slow-2g
         RTT: '250'
         Sec-CH-UA: '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"'
         Sec-CH-UA-Mobile: '?0'
         Sec-CH-UA-Platform: 'Windows'
         Sec-CH-UA-Platform-Version: '10.0'
         Sec-Fetch-Dest: document
         Sec-Fetch-Mode: navigate
         Sec-Fetch-Site: none
         Sec-Fetch-User: '?1'
         Sec-GPC: '1'
         Upgrade-Insecure-Requests: '1'
         User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4389.114 Safari/537.36
         Viewport-Width: '1707'


.. _cookies:

Supplying cookies
-----------------
It is possible to add cookies to HTTP requests for pages that need it, for example:

.. code-block:: yaml

   url: https://example.com/
   cookies:
       Key: ValueForKey
       OtherKey: OtherValue


.. _post:

Using POST request method
-------------------------
The ``POST`` `HTTP request method <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>`__ is used to submit
form-encoded data to the specified resource (server). In :program:`webchanges`, simply supply your data in the ``data``
directive. The ``method`` will be automatically changed to ``POST`` and, if no `Content-type
<https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`__ header is supplied, it will be set to
``application/x-www-form-urlencoded``.

.. code-block:: yaml

   url: https://example.com/
   data:
       Element1: Data
       Element2: OtherData

For a string (e.g. JSON-encoded data, if supported by the server):

.. code-block:: yaml

   url: https://example.com/
   data: '{"Element1": "Data", "Element2": "OtherData"}'


.. _compared_versions:

Comparing with several latest snapshots
---------------------------------------
If a webpage frequently changes between several known stable states, it may be desirable to have changes reported only
if the webpage changes into a new unknown state. You can use ``compared_versions`` to do this:

.. code-block:: yaml

   url: https://example.com/
   compared_versions: 3

In this example, changes are only reported if the webpage becomes different from the latest three distinct states. The
differences are shown relative to the closest match.

.. _ssl_no_verify:

Ignoring SSL errors
-------------------
Setting `ssl_no_verify` to true may be useful during local development or testing.

When set to true, :program:`webchanges` requests will accept any TLS certificate presented by the server, and will
ignore hostname mismatches and/or expired certificates, which will make your application vulnerable to
man-in-the-middle (MitM) attacks.

.. code-block:: yaml

   url: https://example.com/
   ssl_no_verify: true


.. _ignore_errors:

Ignoring connection errors
--------------------------
In some cases, it might be useful to ignore (temporary) network errors to avoid notifications being sent. While there is
a ``display.error`` config option (defaulting to ``true``) to control reporting of errors globally, to ignore network
errors for specific jobs only, you can use the ``ignore_connection_errors`` directive in the job list configuration.
For connection errors during local development or testing due to TLS/SSL use the ``ssl_no_verify`` directive above
instead.

.. code-block:: yaml

   url: https://example.com/
   ignore_connection_errors: true

Similarly, you might want to ignore some (temporary) HTTP errors on the server side:

.. code-block:: yaml

   url: https://example.com/
   ignore_http_error_codes: 408, 429, 500, 502, 503, 504

or ignore all HTTP errors if you like:

.. code-block:: yaml

   url: https://example.com/
   ignore_http_error_codes: 4xx, 5xx


.. _encoding:

Overriding the content encoding
-------------------------------
For web pages with missing or incorrect ``'Content-type'`` HTTP header or whose (rare) encoding cannot be
`correctly guessed <https://docs.python-requests.org/en/master/api/#requests.Response.apparent_encoding>`__
by the `chardet <https://chardet.readthedocs.io/en/latest/faq.html#what-is-character-encoding-auto-detection>`__
library we use, it may be useful to explicitly specify an encoding as defined in Python’s `Standard Encodings
<https://docs.python.org/3/library/codecs.html#standard-encodings>`__ like this:

.. code-block:: yaml

   url: https://example.com/
   encoding: utf-8


Receiving a report every time webchanges runs
---------------------------------------------
If you are watching pages that change seldomly, but you still want to be notified evert time `:program:`webchanges``
runs to know it's still working, you can monitor the output of the ``date`` command, for example:

.. code-block:: yaml

   name: webchanges run
   command: date

Since the output of ``date`` changes every second, this job should produce a report every time webchanges is run.


.. _json_dict:

Selecting items from a JSON dictionary
--------------------------------------
If you are watching JSON-encoded dictionary data but are only interested in the data contained in (a) certain key(s),
you can use the :ref:`jq` filter (Linux/macOS only, ASCII only) to extract it, or write a cross-platform Python command
like the one below:


.. code-block:: yaml

   url: https://example.com/api_data.json
   user_visible_url: https://example.com
   execute: "python3 -c \"import sys, json; print(json.load(sys.stdin)['data'])\""


Escaping of the Python is a bit complex due to being inside a double quoted shell string inside a double quoted YAML
string. For example, ``"`` code becomes ``\\\"`` and ``\n`` becomes ``\\n`` -- and so on. The example below provides
seemingly complex escaping as well how to inform the downstream html reporter that the extracted data is in Markdown:

.. code-block:: yaml

   url: https://example.com/api_data.json
   user_visible_url: https://example.com
   execute: "python3 -c \"import sys, json; d = json.load(sys.stdin); [print(f\\\"[{v['Title']}]\\n({v['DownloadUrl']})\\\") for v in d['value']]\""
   is_markdown: true



Watching changes on .onion (Tor) pages
--------------------------------------
Since pages on the `Tor Network <https://www.torproject.org>`__ are not accessible via public DNS and TCP, you need to
either configure a Tor client as an HTTP/HTTPS proxy or, in Linux/macOS, use the `torify` tool from the `tor` package
(installable using ``apt install tor`` on Debian or Ubuntu or ``brew install tor`` on macOS). Setting up Tor is out of
scope for this document.

If using `torify`, just prefix the :program:`webchanges` command with the `torify` wrapper to access .onion pages:

.. code-block:: bash

   torify webchanges


Watching Facebook page events
-----------------------------
If you want to be notified of new events on a public Facebook page, you can use the following job pattern; just replace
``PAGE`` with the name of the page (can be found by navigating to the events page on your browser):

.. code-block:: yaml

   url: https://m.facebook.com/PAGE/pages/permalink/?view_type=tab_events
   filter:
     - css:
         selector: div#objects_container
         exclude: 'div.x, #m_more_friends_who_like_this, img'
     - re.sub:
         pattern: '(/events/\d*)[^"]*'
         repl: '\1'
     - html2text:
   comparison_filter: additions


Watching GitHub releases and GitLab tags
----------------------------------------
This is an example how to watch the GitHub “releases” page for a given project for the latest release version, to be
notified of new releases:

.. code-block:: yaml

   url: https://github.com/git/git/releases
   filter:
     - xpath: (//div[contains(@class,"release-timeline-tags")]//h4)[1]/a
     - html2text:

This is the corresponding version for GitLab tags:

.. code-block:: yaml

   url: https://gitlab.com/gitlab-org/gitlab/-/tags
   filter:
     - xpath: (//a[contains(@class,"item-title ref-name")])[1]
     - html2text:


Passing diff output to a custom script
--------------------------------------
In some situations, it might be useful to run a script with the diff as input when changes were detected (e.g. to start
an update or process something). This can be done by combining ``diff_filter`` with the ``shellpipe`` filter, which
can run any custom script.

The output of the custom script will then be the diff result as reported by webchanges, so if it outputs any status, the
``CHANGED`` notification that webchanges does will contain the output of the custom script, not the original diff. This
can even have a "normal" filter attached to only watch links (the ``css: a`` part of the filter definitions):

.. code-block:: yaml

   url: https://example.org/downloadlist.html
   filter:
     - css: a
   diff_filter:
     - shellpipe: /usr/local/bin/process_new_links.sh

If running on Linux/macOS, please read about file permission restrictions in the filter's explanation
:ref:`here <shellpipe>`.

.. _word_based_differ:

Using word-based differ (``wdiff``)
-----------------------------------
You can also specify an **external** ``diff``-style tool (a tool that takes two filenames (old, new) as parameter and
returns the difference of the files on its standard output). For example, to to get word-based differences instead of
line-based difference, use GNU ``wdiff``:

.. code-block:: yaml

   url: https://example.com/
   diff_tool: wdiff

In order for this to work, ``wdiff`` needs to  be installed separately (e.g. ``apt install wdiff`` on Debian/Ubuntu,
``brew install wdiff`` on macOS, or download from `here <https://www.di-mgt.com.au/wdiff-for-windows.html>`__ for
Windows).

When using ``diff_tool: wdiff`` with an ``html`` report, the output of ``wdiff`` will be colorized.

Note: the use of an external differ will override the ``diff`` setting of the ``html`` report.


.. _chromium_revision:

Using a Chromium revision matching a Google Chrome / Chromium release
---------------------------------------------------------------------
`:program:`webchanges`` currently specifies a Chromium release equivalent to Google Chrome version 89.0.4389.72.  If you
want a different one, you can do so, but unfortunately the Chromium revision number does not match the Google Chrome /
Chromium release one.

There are multiple ways of finding what the revision number is for a stable Chrome release; the
one I found easiest is to go to https://chromium.cypress.io/, selecting the "stable" release channel `for the OS you
need`, and clicking on "get downloads" for the one you want. At the top you will see something like "Base revision:
843830. Found build artifacts at 843831 [browse files]". You want the revision with build artifacts, in this example
843831.

Be aware that the same Google Chrome / Chromium release may be based on a different Chromium revision on different OSs,
and that not all Chromium revisions are available for all OS platforms (Linux_x64, Mac, Win and Win_x64). The full
list of revisions available for download by `Pyppeteer` is at
https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html.
Specifying a release number that is not available for download is the cause of a ``zipfile.BadZipFile: File is not a zip
file`` error from the `Pyppeteer` code.

Please note that every time you change the chromium_revision, a new download is initiated and the old version is kept
on your system, using up space. If you no longer need it you need to delete it manually; the the directory where it is
stored can be found by running ``python3 -c "from pyppeteer.chromium_downloader import DOWNLOADS_FOLDER;
print(DOWNLOADS_FOLDER)"``

To specify the Chromium revision to use (and other defaults) globally, edit config.yaml:

.. code-block:: yaml

   job_defaults:
     browser:
       chromium_revision:
         linux: 843831
       switches:
         - --enable-experimental-web-platform-features
         - '--window-size=1298,1406'

To specify the same on an individual job:

.. code-block:: yaml

   url: https://example.com/
   use_browser: true
   chromium_revision:
     linux: 843831
   switches:
     - --enable-experimental-web-platform-features
     - '--window-size=1298,1406'


If you use multiple OSs, you can specify different Chromium revisions to use based on the OS `:program:`webchanges`` is
running in by using a dict with one or more of ``linux``, ``mac``, ``win32`` and/or ``win64`` keys, either as a global
default (like below) or in individual jobs:

.. code-block:: yaml

   job_defaults:
     browser:
       chromium_revision:
         linux: 843831
         win64: 843846
         win32: 843832
         mac: 843846


.. _pyppeteer_target_closed:

Running ``use_browser: true`` jobs in low-memory environments
-------------------------------------------------------------
In certain Linux environments with limited memory, jobs with ``use_browser: true`` may fail with a
``pyppeteer.errors.NetworkError: Protocol error Runtime.callFunctionOn: Target closed.`` error.

In such cases, try adding the `--disable-dev-shm-usage
<https://peter.sh/experiments/chromium-command-line-switches/#disable-dev-shm-usage>`__ Chromium switch in the config
file as follows:

.. code-block:: yaml

   job_defaults:
     browser:
       switches:
         - --disable-dev-shm-usage

This switch disables the use of the faster RAM-based temporary storage file system, whose size limit may cause Chromium
to crash, forcing instead the use of the drive-based filesystem, which may be slower but of ampler capacity.


.. _local_storage:

Browsing websites using local storage for authentication
---------------------------------------------------------
Some sites don't use cookies for authentication but store their functional equivalent using 'Local Storage'.  In these
circumstances, you can use :program:`webchanges` with ``use_browser: true`` directive and its ``user_data_dir``
sub-directive to instruct it to use a pre-existing user directory.

Specifically:

#. Create an empty directory somewhere (e.g. ``/userdir``)
#. Run Chromium Google Chrome browser with the ``--user-data-dir`` switch pointing to this directory (e.g. ``chrome.exe
   --user-data-dir=/userdir``)
#. Browse to the site that you're interested in tracking and log in or do whatever is needed for it to save the
   authentication data in local storage
#. Exit the browser

You can now run a :program:`webchanges` job defined like this:

.. code-block:: yaml

   url: https://example.org/usedatadir.html
   use_browser: true
   user_data_dir: /userdir

.. _pyppeteer_block_elements:

Speeding up ``use_browser: true`` jobs with ``block_elements``
--------------------------------------------------------------

⚠ Experimental: on certain sites this seems to totally freeze execution; test before use

If you're not interested in all elements of a website, you can skip downloading the ones that you don't care, paying
attention to do some testing as some elements may be required for the correct rendering of the website. Typical elements
to skip include ``stylesheet``, ``font``, ``image``, and ``media`` (but use with caution) and can be specified like
this on a job-by-job basis:

.. code-block:: yaml

   name: This is a Javascript site
   note: It's just a test
   url: https://www.example.com
   use_browser: true
   block_elements:
     - stylesheet
     - font
     - image
     - media

or in the config file (for all ``use_browser: true`` jobs):

.. code-block:: yaml

   job_defaults:
     browser:
       block_elements:
         - stylesheet
         - font
         - image
         - media
