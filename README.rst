Welcome to Telegritter
======================

**Telegritter** is a Telegram to Twitter bridge, in other words a Tegram user interface to your Twitter account.


.. image:: media/logo_256.png


It's essentially a Telegram bot whom with you chat and makes you interact with Twitter.

So if you write to the bot, it tweets. If you send it images, those get tweeted. If your messages got replied or you get messaged in Twitter, the bot will talk that to you. You can answer that, of course, guess what happens??? Yes, it gets tweeted! You know the drill.

It even manages direct messages (DMs), marking received messages with a prefix so they are


How to use it
-------------

Make it run, add the bot to your Telegram account, start talking/tweeting.

The first time you talk to the bot through Telegram, Telegritter will save your user id and will forbid other users to use it. You don't need to save your user id as a specific step, it's automatic.


How to make it run
------------------

There are threee three parts in making Telegritter live: have the process running, make it talk to Twitter, and make it talk to Telegram. Once these three are done, you can leave it running and enjoy it.

Note: these instructions does not cover how to install this in a deamon mode, supporting machine reboots, etc. PRs welcomed.

So, first, have the process running. You only need to have `fades <https://github.com/PyAr/fades>`_ installed. After cloning the project, prepare the authentication files (see the section below) and run::

    ./run <path to telegram auth file> <path to twitter auth file>


How to try it's working
-----------------------

At this point you should be able to write something in Telegram and see that tweetted. Try answering that tweet and you should receive the new message back on Telegram.


Configuration Setup
===================

The configuration setup is basically getting the auth tokens for Telegram and Twitter, and saving them in somewhat secure files for the program to use them (using `infoauth <https://pypi.org/project/infoauth/>`_).


Configuring Telegram
--------------------

Open your Telegram client, search for BotFather and start talking to it. 

First step is to create the bot you will use for this, so tell the following to BotFather::

  /newbot 

It will ask for a name, and then for an username. Example: ``Telegritter Example`` and ``telegritter_example_bot``.  Note that because of Telegram rules, the name you choose needs to end in 'bot'.

If all is fine, Botfather should congratulate you and give you a token to access the HTTP API, something that would look like ``4121309109:j2ETwMFpwk1ldaj39jdaaj4vWoe7Kqv-ee1``.

Copy that string and save it using ``infoauth``::

    infoauth create telegritter-telegram.cfg token=4121309109:j2ETwMFpwk1ldaj39jdaaj4vWoe7Kqv-ee1


Configuring Twitter
-------------------

Open Twitter in your browser, and being logged into your account, go to `the section for developers to manage applications <https://developer.twitter.com/en/apps/>`_.

There you would be able to create a new application, and after filling quite some information you will have access to the "Keys and tokens" section, where you will find the consumer API keys, something like::

    API key: ldaeiddlh3o8ahdl.SDA?DJAV
    API secret key: CJDWa;dj3laohdlaohdl8ohdl8ohdlohlhaddhflkshflkfWfz

...and access tokens, something like::

    Access token: 41225dl73qoy8hd94fsf-sn4fnej2q8hadaliASD4fwrKeED1r
    Access token secret: dljo8maod38hd8hldi3aflaodaHFOULUEGlidshfshfoz

Grab all those for ugly strings and save them using ``infoauth``::

    infoauth create telegritter-twitter.cfg \
        api_key=ldaeiddlh3o8ahdl.SDA?DJAV \
        api_secret_key=CJDWa;dj3laohdlaohdl8ohdl8ohdlohlhaddhflkshflkfWfz \
        access_token=41225dl73qoy8hd94fsf-sn4fnej2q8hadaliASD4fwrKeED1r \
        access_token_secret=dljo8maod38hd8hldi3aflaodaHFOULUEGlidshfshfoz
