Welcome to telegritter
======================

``telegritter`` is a Telegram to Twitter bridge, in other words a Tegram user interface to your Twitter account.


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

So, first, have the process running. You only need to have `fades <https://github.com/PyAr/fades>`_ installed. Clone the project and just::

    ./run

You should get an ERROR because of auth needed for Telegram. Let's fix that. Go to **Configuring Telegram** section below and come back when finished.

If you `./run` the project again you should get another ERROR, now it's turn for Twitter. Go to **Configuring Twitter** section below, and come back when finished.

FIXME:
que corra de nuevo, debería QUE??
como probarlo que funciona??


Configuring Telegram
--------------------

Open your Telegram client, search for BotFather and start talking to it. 

First step is to create the bot you will use for this, so tell the following to BotFather::

  /newbot 

It will ask for a name, and then for an username. Example: ``Telegritter Example`` and ``telegritter_example_bot``.  Note that because of Telegram rules, the name you choose needs to end in 'bot'.

If all is fine, Botfather should congratulate you and give you a token to access the HTTP API, something that would look like ``4121309109:j2ETwMFpwk1ldaj39jdaaj4vWoe7Kqv-ee1``.

Copy that string and tell telegritter that this is the Telegram token::

    ./run --telegram-token=4121309109:j2ETwMFpwk1ldaj39jdaaj4vWoe7Kqv-ee1

And that's all!


Configuring Twitter
-------------------

Open Twitter in your browser, and being logged into your account, go to `the section for developers to manage applications <https://developer.twitter.com/en/apps/>`_.

There you would be able to create a new application, and after filling quite some information you will have access to the "Keys and tokens" section, where you will find the consumer API keys, something like...

    API key: ldaeiddlh3o8ahdl.SDA?DJAV
    API secret key: CJDWa;dj3laohdlaohdl8ohdl8ohdlohlhaddhflkshflkfWfz

...and access tokens, something like...

    Access token: 41225dl73qoy8hd94fsf-sn4fnej2q8hadaliASD4fwrKeED1r
    Access token secret: dljo8maod38hd8hldi3aflaodaHFOULUEGlidshfshfoz

Grab all those for ugly strings, get them together separated by ``:``, 
        consumer_key, consumer_secret, access_token, access_token_secret = tokens
