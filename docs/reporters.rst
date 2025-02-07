.. _reporters:

=========
Reporters
=========
By default :program:`webchanges` prints out information about changes to the data collected to standard output
(``stdout``), which is your terminal if you run it interactively (If running via `cron` or another scheduler service,
the destination of this output depends on the scheduler and its configuration).

You can change the settings to change or add to where the report is sent to.  Settings are contained in the
configuration file ``config.yaml``, a text file located in the ``~/.config/webchanges`` directory for Linux or macOS,
or in the `:program:`webchanges`` folder within your Documents folder (i.e. ``%USERPROFILE%\Documents\webchanges``) for
Windows, and is editable using any text editor or with the command ``webchanges --edit--config``.  The configuration
for the reporters will be listed under the ``reporters`` section.

.. note::
   The ``config.yaml`` file is created at the first run of ``webchanges --edit`` or ``webchanges --edit--config``.

.. tip:: To test a reporter, use the ``--test-reporter`` command-line option with the name of the reporter, e.g.
   ``webchanges --test-reporter stdout``

:program:`webchanges` will generate test  ``new``, ``changed``, ``unchanged`` and ``error`` notifications and send (the
ones configured to be sent under ``display``) via the ``stdout`` reporter (if it is enabled). Any reporter that is
configured and enabled can be tested. To test if your email reporter is configured correctly, you use::

   webchanges --test-reporter email

If the test does not work, check your configuration and/or add the ``--verbose`` command-line option to show
detailed debug logs::

   webchanges --verbose --test-reporter email

At the moment, the following reporters are available

* :ref:`stdout` (enabled by default): Display summary on stdout (the console)
* :ref:`browser`: Display summary on the default web browser
* :ref:`email`: Send summary via email (including SMTP)
* :ref:`xmpp`: Send a message using the Extensible Messaging and Presence Protocol (XMPP)
* :ref:`webhook`: Send a message to a Slack or Discord channel using the service's webhook
* :ref:`telegram`: Send a message using Telegram
* :ref:`pushbullet`: Send summary via pushbullet.com
* :ref:`pushover`: Send summary via pushover.net
* :ref:`ifttt`: Send summary via IFTTT
* :ref:`matrix`: Send a message to a room using the Matrix protocol
* :ref:`mailgun`: Send email via the Mailgun service
* :ref:`prowl`: Send a message via prowlapp.com

.. To convert the "webchanges --features" output, use:
   webchanges --features | sed -e 's/^  \* \(.*\) - \(.*\)$/- **\1**: \2/'

Each reporter has a directive called ``enabled`` that can be toggled (true/false).


Please note that many reporters need the installation of additional Python packages to work, as noted below and in
:ref:`dependencies`.


.. _browser:

Browser
-------
Displays the summary in HTML format using the system's default web browser


.. _email:

Email
-----
Sends email, via smtp or sendmail.

Sub-directives
~~~~~~~~~~~~~~
* ``method``: Either `smtp` or `sendmail`
* ``from``: The sender's email address. **Do not use your main email address** but create a throwaway one!
* ``to``: The destination email address
* ``subject``: The subject line. Use {count} for the number of reports, {jobs} for the titles of the jobs reported
* ``html``: Whether the email includes HTML (true/false)


.. _smtp:

SMTP
~~~~

Login with plaintext password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can save a password in the ``insecure_password`` directive in the SMTP to enable unattended scheduled runs of
:program:`webchanges`. As the name says, storing the password as plaintext in the configuration is insecure and bad
practice, yet for a throwaway account that is only used for sending these reports this might be a low-risk way to run
unattended.

**Never ever use this method with your your primary email account!**  Seriously! Create a throw-away free email
account just for sending out these emails; see below for an example on how to do so with :ref:`Gmail <gmail>`.

Example:

.. code-block:: yaml

   report:
     email:
     enabled: true
     from: 'webchanges <throwawayaccount@example.com>'  # (edit accordingly; don't use your primary account for this!!)
     to: 'myself@example.com'  # The email address of where want to receive reports
     subject: '[webchanges] {count} changes: {jobs}'
     html: true
     method: 'smtp'
       host: 'smtp.example.com'
       user: 'throwawayaccount@example.com'  # (edit accordingly; don't use your primary account for this!!)
       port: 587
       starttls: true
       auth: true
       insecure_password: 'this_is_my_secret_password'

Once again, note that this makes it really easy for your password to be picked up by software running on your machine,
by other users logged into the system and/or for the password to appear in log files accidentally, so it's **insecure**.


.. _smtp-login-with-keychain:

Login with keyring
^^^^^^^^^^^^^^^^^^^
A secure way to store your password is to use a keyring by running ``webchanges --smtp-login`` after configuring your
``host`` and ``user``; this requires installing the optional ``safe_password`` dependencies (see optional packages
below). Be aware that the use of keyring won't allow you to run :program:`webchanges` unattended (e.g. from a
scheduler). If you're using a keychain, the ``insecure_password`` key is ignored and can be left blank.


SMTP sub-directives
^^^^^^^^^^^^^^^^^^^
* ``host``: The address of the SMTP server
* ``port``: The port used to communicate with the server
* ``starttls``: Whether the server uses SSL/TLS encryption (true/false)
* ``auth``: Whether authentication via username/password is required (true/false)
* ``user``: The username used to authenticate
* ``insecure_password``: The password used to authenticate (if no keyring)

.. _gmail:

Gmail example
^^^^^^^^^^^^^
WARNING: You **do not want to do this with your primary Google account**, but rather get a free separate one just for
sending mails from :program:`webchanges` and similar programs. Allowing less secure apps and storing the password (even
if it's in the keychain) is not good security practice for your primary account. You have been warned!

First configure your Gmail account to allow for "less secure" (password-based) apps to login:

#. Go to https://myaccount.google.com/
#. Click on "Security"
#. Scroll all the way down to "less secure apps access" and turn it on

Then configure these directives as follows:

.. code-block:: yaml

   report:
     email:
       enabled: true
       from: 'your.username@gmail.com'  # (edit accordingly; don't use your primary account for this!!)
       to: 'your.destination@example.org'  # The email address of where want to receive reports
       subject: '[webchanges] {count} changes: {jobs}'
       html: true
       method: 'smtp'
         host: 'smtp.gmail.com'
         user: 'your.username@gmail.com'  # (edit accordingly; don't use your primary account for this!!)
         port: 587
         starttls: true
         auth: true
         insecure_password: 'this_is_my_secret_password'

Amazon Simple Email Service (SES) example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First ensure that you have configured SES as per the `Quick start
<https://docs.aws.amazon.com/ses/latest/DeveloperGuide/quick-start.html>`__

Create a user just for :program:`webchanges` for security reasons (so you can easily recover from a compromised
user/password leak from, e.g. from a scan of your jobs file), then configure these directives as follows:

.. code-block:: yaml

   report:
     email:
       enabled: true
       from: you@verified_domain.com  # (edit accordingly)
       to: your.destination@example.org  # The email address you want to send reports to
       subject: '{count} changes: {jobs}'
       html: true
       method: smtp
         host: email-smtp.us-west-2.amazonaws.com  # (edit accordingly)
         user: ABCDEFGHIJ1234567890  # (edit accordingly)
         insecure_password: 'this_is_my_secret_password'  # (edit accordingly)
         auth: true
         port: 587  # (25 or 465 also work)
         starttls: true


.. _sendmail:

sendmail
~~~~~~~~

Calls the external `sendmail <https://www.proofpoint.com/us/products/email-protection/open-source-email-solution>`__
program, which must already be installed and configured.


Optional packages
~~~~~~~~~~~~~~~~~
If using a keychain to store the password, you also need to:

* Install the ``safe_password`` :ref:`optional package <optional_packages>` as per below
* Install all the dependencies of the ``keyring`` package as per documentation `here
  <https://pypi.org/project/keyring/>`_
* Configure the ``keyring`` package to use the keychain backend being used in your system following the instructions
  on the same page

.. code-block:: bash

   pip install --upgrade webchanges[safe_password]


.. _ifttt:

IFTTT
-----
To configure IFTTT events, you need to retrieve your key from `<https://ifttt.com/maker_webhooks/settings>`__.

The URL shown in "Account Info" has the following format:

.. code::

   https://maker.ifttt.com/use/{key}

In this URL, ``{key}`` is your API key. The configuration should look like this (you can pick any event name you want):

.. code:: yaml

   ifttt:
     enabled: true
     key: aA12abC3D456efgHIjkl7m
     event: event_name_you_want

The event will contain three values in the posted JSON:

* ``value1``: The type of change (``new``, ``changed``, ``unchanged`` or ``error``)
* ``value2``: The name of the job (``name`` directive in ``jobs.yaml``)
* ``value3``: The location of the job (``url`` or ``command`` directive in ``jobs.yaml``)

These values will be passed on to the Action in your Recipe.

IFTT uses the :ref:`text` report type.


.. _mailgun:

Mailgun
-------
Sends email using the commercial `Mailgun <https://www.mailgun.com/>`__ service.


Sub-directives
~~~~~~~~~~~~~~
* ``domain``: The domain
* ``api_key``: API key (see `here
  <https://help.mailgun.com/hc/en-us/articles/203380100-Where-Can-I-Find-My-API-Key-and-SMTP-Credentials->`__)
* ``from_name``: Sender's name
* ``from_mail``: Sender's email address
* ``to``: Recipient's email address
* ``subject``: The subject line. Use {count} for the number of reports, {jobs} for the titles of the jobs reported
* ``region`` (optional)

Mailgun uses the :ref:`text` report type.


.. _matrix:

Matrix
------
Sends notifications through the `Matrix protocol <https://matrix.org>`__.

You first need to register a Matrix account for the bot on any home server.

You then need to acquire an access token and room ID, using the following instructions adapted from `this
guide <https://t2bot.io/docs/access_tokens/>`__:

1. Open `Riot.im <https://riot.im/app/>`__ in a private browsing window
2. Register/Log in as your bot, using its user ID and password.
3. Set the display name and avatar, if desired.
4. In the settings page, select the "Help & About" tab, scroll down to the bottom and click Access Token:
   <click to reveal>.
5. Copy the highlighted text to your configuration.
6. Join the room that you wish to send notifications to.
7. Go to the Room Settings (gear icon) and copy the *Internal Room ID* from the bottom.
8. Close the private browsing window **but do not log out, as this invalidates the Access Token**.

Here is a sample configuration:

.. code:: yaml

   matrix:
     enabled: true
     homeserver: https://matrix.org
     access_token: 'YOUR_TOKEN_HERE'
     room_id: '!roomroomroom:matrix.org'

You will probably want to use the following configuration for the ``markdown`` reporter, if you intend to post change
notifications to a public Matrix room, as the messages quickly become noisy:

.. code:: yaml

   markdown:
     enabled: true
     details: false
     footer: false
     minimal: true

Matrix uses the :ref:`text` report type.


.. _pushbullet:

Pushbullet
----------
Pushbullet notifications are configured similarly to Pushover (see above). You’ll need to add to the config your
Pushbullet Access Token, which you can generate at https://www.pushbullet.com/#settings

Required packages
~~~~~~~~~~~~~~~~~
To use this report you need to install :ref:`optional_packages`. Install them using:

.. code-block:: bash

   pip install --upgrade webchanges[pushbullet]

Pushbullet uses the :ref:`text` report type.

.. _pushover:

Pushover
--------
You can configure webchanges to send real time notifications about changes via `Pushover <https://pushover.net/>`__.
To enable this, ensure you
have the ``chump`` python package installed (see :doc:`dependencies`). Then edit your config (``webchanges
--edit-config``) and enable pushover. You will also need to add to the config your Pushover user key and a unique app
key (generated by registering webchanges as an application on your `Pushover account
<https://pushover.net/apps/build>`__.

You can send to a specific device by using the device name, as indicated when you add or view your list of devices in
the Pushover console. For example ``device:  'MyPhone'``, or ``device: 'MyLaptop'``. To send to *all* of your devices,
set ``device: null`` in your config (``webchanges --edit-config``) or leave out the device configuration completely.

Setting the priority is possible via the ``priority`` config option, which can be ``lowest``, ``low``, ``normal``,
``high`` or ``emergency``. Any other setting (including leaving the option unset) maps to ``normal``.

Pushover uses the :ref:`text` report type.

Required packages
~~~~~~~~~~~~~~~~~
To use this report you need to install :ref:`optional_packages`. Install them using:

.. code-block:: bash

   pip install --upgrade webchanges[pushover]



.. _stdout:

stdout
------
Displays the summary in text format on stdout (the console)

stdout uses the :ref:`text` report type.

Optional sub-directives
~~~~~~~~~~~~~~~~~~~~~~~
* ``color``: Uses color (green for additions, red for deletions) (true/false)



.. _telegram:

Telegram
--------
Telegram notifications are configured using the Telegram `Bot API <https://core.telegram.org/bots>`__).

To set up Telegram, from your Telegram app chat up BotFather (New Message, Search, “BotFather”), then say ``/newbot``
and follow the instructions. Eventually it will tell you the bot token (in the form ``<number>:<random string>``); add
it to your configuration file (run ``webchanges --edit-config``) as below, and save the file.

.. code:: yaml

   telegram:
     enabled: true  # don't forget to set this to true! :)
     bot_token: '999999999:3tOhy2CuZE0pTaCtszRfKpnagOG8IQbP5gf'  # replace your bot api token
     chat_id: ''  # empty for now

Next click on the link of your bot (starts with https://t.me/) and, on the new screen, click on start (which will send
the message ``/start``) and enter any text ("Hello" is fine).  Then run ``webchanges --telegram-chats``, which will list
the private chats the bot is involved with. This will list the chat ID that you need to put into the configuration
file (run ``webchanges --edit-config``) as ``chat_id``:

.. code:: yaml

   telegram:
     enabled: true
     bot_token: '999999999:3tOhy2CuZE0pTaCtszRfKpnagOG8IQbP5gf'  # replace with your bot api token
     chat_id: 88888888  # the chat id where the messages should be sent
     silent: false  # set to true to receive a notification with no sound

You may add multiple chat IDs as a YAML list:

.. code:: yaml

   telegram:
     enabled: true
     bot_token: '999999999:3tOhy2CuZE0pTaCtszRfKpnagOG8IQbP5gf'  # your bot api token
     chat_id:
       - 11111111
       - 22222222
     silent: true  # set to false to receive a notification with sound

Telegram uses the :ref:`markdown` report type.

Optional sub-directives
~~~~~~~~~~~~~~~~~~~~~~~
* ``silent``: Receive a notification with no sound (true/false) (default: false)


.. versionchanged:: 3.7
   Added `silent` sub-directive and switched from the `text` to the `markdown` report type.

.. _webhook:

Webhook (Slack, Discord, Mattermost etc.)
-----------------------------------------
Services such as Slack, Discord, Mattermost etc. that support incoming webhooks can be used for notifications using the
``webhook`` or ``webhook_markdown`` reporters:

.. code:: yaml

   webhook:
     enabled: true
     webhook_url: https://hooks.slack.com/services/T50TXXXXXU/BDVYYYYYYY/PWTqwyFM7CcCfGnNzdyDYZ

``webhook`` uses the :ref:`text` report type, while ``webhook_markdown`` uses the :ref:`markdown` one.

Slack
~~~~~
To set up Slack, create a new Slack app in the workspace where you want to post messages, toggle **Activate Incoming
Webhooks** on in the Features page, click **Add New Webhook to Workspace**, pick a channel that the app will post to,
then click **Authorize** (see `here
<https://slack.com/intl/en-sg/help/articles/115005265063-Incoming-webhooks-for-Slack>`__). Copy the webhook URL and
paste it into the configuration as seen above.

.. versionchanged:: 3.0.1
   Renamed from ``slack`` to ``webhook``

Discord
~~~~~~~
To set up Discord, from your Discord server settings select Integration and create a "New Webhook", give the
webhook a name to post under, select a channel, press on "Copy Webhook URL" and paste the URL into the configuration as
seen below (see `here <https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks>`__).

.. code:: yaml

   webhook:
     enabled: true
     webhook_url: https://discordapp.com/api/webhooks/11111XXXXXXXXXXX/BBBBYYYYYYYYYYYYYYYYYYYYYYYyyyYYYYYYYYYYYYYY

Mattermost
~~~~~~~~~~
To set up Mattermost follow the documentation `here <https://docs.mattermost.com/developer/webhooks-incoming.html>`__
to generate a webhook URL and paste it into the configuration as such (note that Mattermost prefers markdown so we're
using the ``webhook_markdown`` variant):

.. code:: yaml

   webhook_markdown:
     enabled: true
     webhook_url: http://{your-mattermost-site}/hooks/xxx-generatedkey-xxx

Sub-directives
~~~~~~~~~~~~~~
* ``webhook_url`` (required): the webhook URL
* ``max_message_length``: the maximum length of a message in characters (default: 40,000, unless ``webhook_url`` starts
  with \https://discordapp.com, then 2,000). `New in version 3.0.`

.. versionchanged:: 3.0.1
   Added ``webhook_markdown`` variant



.. _xmpp:

XMPP
----
You can have notifications sent to you through the `XMPP protocol`.

To achieve this, you should register a new XMPP account that is just used for :program:`webchanges`.

Here is a sample configuration:

.. code:: yaml

   xmpp:
     enabled: true
     sender: 'BOT_ACCOUNT_NAME'
     recipient: 'YOUR_ACCOUNT_NAME'

You can store your password securely on a keychain if you have one installed by running ``webchanges --xmpp-login``;
this also requires having the optional ``safe_password`` dependencies installed (see below).  However, be aware that
the use of safe password and ``keyring`` won't allow you to run :program:`webchanges` unattended (e.g. from a
scheduler), so you can save the password in the ``insecure_password`` directive in the XMPP config instead:

.. code-block:: yaml

   report:
     xmpp:
       enabled: true
       sender: 'BOT_ACCOUNT_NAME'
       recipient: 'YOUR_ACCOUNT_NAME'
       insecure_password: 'this_is_my_secret_password'

As the name says, storing the password as plaintext in the configuration is insecure and bad practice, yet for an
account that only sends these reports this might be a low-risk way.

XMPP uses the :ref:`text` report type.

Required packages
~~~~~~~~~~~~~~~~~
To run jobs with this reporter, you need to install :ref:`optional_packages`. Install them using:

.. code-block:: bash

   pip install --upgrade webchanges[xmpp]

Optional packages
~~~~~~~~~~~~~~~~~
If using a keychain to store the password, you also need to:

* install the ``safe_password`` :ref:`optional package <optional_packages>` as per below,
* install all the dependencies of the ``keyring`` package as per documentation `here
  <https://pypi.org/project/keyring/>`_,
* configure the ``keyring`` package to use the keychain backend you're using in your system following the instructions
  on the same page.

.. code-block:: bash

   pip install --upgrade webchanges[safe_password]



.. _prowl:

Prowl
-----

You can have notifications sent to you through the `Prowl <https://www.prowlapp.com>`__ push notification service to
receive the notification on iOS (only).

To achieve this, you should register a new Prowl account, and have the Prowl application installed on your iOS device.

To create an API key:

1. Log into the Prowl website at https://www.prowlapp.com/api_settings.php
2. If needed, navigate to the "API Keys" tab.
3. Scroll to the "Generate a new API key" section.
4. Give the key a note that will remind you you've used it for this service.
5. Press "Generate Key".
6. Copy the resulting key.

Here is a sample configuration:

.. code:: yaml

   prowl:
     enabled: true
     api_key: '<your api key here>'
     priority: 2
     application: 'webchanges example'
     subject: '{count} changes: {jobs}'

The "subject" field will be used as the name of the Prowl event. The application field is prepended to the event and
shown as the source of the event in the Prowl App.

Prowl uses the :ref:`text` report type.

`Added in version 3.0.1:`
