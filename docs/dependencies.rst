.. _dependencies:

============
Dependencies
============

.. _optional_packages:

Optional packages
-----------------
Certain features require additional Python packages to work. These optional packages are installed by appending
to the name `webchanges` the name of the feature (from the table below) inside square brackets, like so::

    pip install --upgrade webchanges[use_browser]
    pip install --upgrade webchanges[use_browser,redis]

+-------------------------+-------------------------------------------------------------------------+
| Feature                 | Python package(s) installed                                             |
+=========================+=========================================================================+
| ``use _browser`` set to | * `pyppeteer <https://github.com/pyppeteer/pyppeteer>`__                |
| true (in a url job)     | * Note: you may also have to **separately install**                     |
|                         |   OS-specific dependencies [#f1]_                                       |
+-------------------------+-------------------------------------------------------------------------+
| ``bs4`` method of the   | * `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__   |
| html2text filter        |                                                                         |
|                         |                                                                         |
+-------------------------+-------------------------------------------------------------------------+
| ``beautify`` filter     | * `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__   |
|                         | * `jsbeautifier <https://pypi.org/project/jsbeautifier/>`__ [#f2]_      |
|                         | * `cssbeautifier <https://pypi.org/project/cssbeautifier/>`__ [#f3]_    |
+-------------------------+-------------------------------------------------------------------------+
| ``pdf2text`` filter     | * `pdftotext <https://github.com/jalan/pdftotext>`__                    |
|                         | * Note: you will also have to **separately install** the required       |
|                         |   OS-specific dependencies [#f4]_                                       |
+-------------------------+-------------------------------------------------------------------------+
| ``ocr`` filter          | * `pytesseract <https://github.com/madmaze/pytesseract>`__              |
|                         |   Note: requires Tesseract to be **separately installed** [#f5]_        |
|                         | * `Pillow <https://python-pillow.org>`__                                |
+-------------------------+-------------------------------------------------------------------------+
| ``ical2text`` filter    | * `vobject <https://eventable.github.io/vobject/>`__                    |
+-------------------------+-------------------------------------------------------------------------+
| ``pushover`` reporter   | * `chump <https://github.com/karanlyons/chump/>`__                      |
+-------------------------+-------------------------------------------------------------------------+
| ``pushbullet`` reporter | * `pushbullet.py <https://github.com/randomchars/pushbullet.py>`__      |
+-------------------------+-------------------------------------------------------------------------+
| ``matrix`` reporter     | * `matrix_client <https://github.com/matrix-org/matrix-python-sdk>`__   |
+-------------------------+-------------------------------------------------------------------------+
| ``xmpp`` reporter       | * `aioxmpp <https://github.com/horazont/aioxmpp>`__                     |
+-------------------------+-------------------------------------------------------------------------+
| ``redis`` database      | * `redis <https://github.com/andymccurdy/redis-py>`__                   |
+-------------------------+-------------------------------------------------------------------------+
| ``safe_password``       | * `keyring <https://github.com/jaraco/keyring>`__                       |
| storage for email and   |                                                                         |
| xmpp reporters          |                                                                         |
+-------------------------+-------------------------------------------------------------------------+
| ``all``                 | * all the optional packages listed above                                |
|                         | * Note: you will also have to **separately install** the required       |
|                         |   OS-specific dependencies [#f1]_ [#f4]_ [#f5]_                         |
+-------------------------+-------------------------------------------------------------------------+

.. rubric:: Footnotes

.. [#f1] ``pyppeteer``'s OS-specific dependencies (only Linux requires them) are listed `here
   <https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix>`__
   (yes, it's a page from puppeteer, which is the project upon which pyppeteer is created).  A missing dependency is
   often the cause of the error ``pyppeteer.errors.BrowserError: Browser closed unexpectedly``.  Also pay close
   attention to the documentation if you're running in `Docker
   <https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#running-puppeteer-in-docker>`__ or other
   specialized environments.
.. [#f2] Optional, to beautify content of <script> tags
.. [#f3] Optional, to beautify content of <style> tags
.. [#f4] see `here <https://github.com/jalan/pdftotext#os-dependencies>`__
.. [#f5] see `here <https://tesseract-ocr.github.io/tessdoc/Installation.html>`__


Installed packages
------------------
These Python packages are installed automatically by `pip`:

* `appdirs <https://github.com/ActiveState/appdirs>`__
* `cssselect <https://github.com/scrapy/cssselect>`__ (required by lxml.cssselect)
* `html2text <https://github.com/Alir3z4/html2text>`__
* `lxml <https://lxml.de>`__
* `markdown2 <https://github.com/trentm/python-markdown2>`__
* `msgpack <https://msgpack.org/>`__
* `PyYAML <https://pyyaml.org/>`__
* `requests <https://requests.readthedocs.io/>`__
* `colorama <https://github.com/tartley/colorama>`__  (only in Windows installations)
