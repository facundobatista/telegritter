# Copyright 2017-2019 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://github.com/facundobatista/telegritter

import asyncio
import logging

import tweepy

from telegritter.config import config

logger = logging.getLogger(__name__)


class Tweet:
    """The tweet processed."""

    def __init__(self, tweet_id, text=None, created_at=None, author=None, useful=True):
        self.tweet_id = tweet_id
        self.useful = useful
        self.text = text
        self.created_at = created_at
        self.author = author

    @classmethod
    def _from_update(cls, update):
        """Create from a twitter message."""
        # FIXME(3): support tweets with images, send them to telegram
        # FIXME(4): differentiate a DM and send it special to telegram

        return cls(tweet_id=update.id, created_at=update.created_at, text=update.text,
                   author=update.author.name)

    @classmethod
    def from_update(cls, update):
        """Securely parse from update."""
        try:
            item = cls._from_update(update)
        except Exception as exc:
            logger.exception("Problem parsing tweet from update: %s", exc)
            item = None

        if item is None:
            # bad parsing, crash in _from_update, user not allowed, etc
            item = cls(tweet_id=update.id, useful=False)
        return item

    def __str__(self):
        template = "<Tweet [{tweet_id}] {text!r} ({author!r}, {created_at})>"
        return template.format(**self.__dict__)


class Twitter:

    def init(self):
        tokens = config.TWITTER_TOKENS.split(':')
        consumer_key, consumer_secret, access_token, access_token_secret = tokens
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def update(self, text):
        """Send message to Twitter."""
        # FIXME(5): run in a thread!!!
        print("================== twitter update, text", repr(text))
        resp = self.api.update_status(text)
        print("================== twitter update, resp", resp)

    async def get(self):
        """Get messages, notifications, etc. from Twitter."""
        # prepare the kwargs
        kwargs = {}
        if config.TWITTER_LAST_ID is not None:
            kwargs['since_id'] = config.TWITTER_LAST_ID
        logger.debug("Getting updates, kwargs=%s", kwargs)

        # get the info from twitter
        loop = asyncio.get_event_loop()
        try:
            items = await loop.run_in_executor(
                None, lambda: self.api.mentions_timeline(**kwargs))
        except tweepy.error.TweepError as exc:
            logger.error("Tweepy error: %s", exc)
            return []

        # log and simple exit
        logger.debug("Twitter mentions results ok! len=%d", len(items))
        if not items:
            return []

        # process results and save last id
        results = []
        for item in items:
            logger.debug("Processing result: %s", item)
            tweet = Tweet.from_update(item)
            if tweet.useful:
                results.append(tweet)
        config.TWITTER_LAST_ID = tweet.tweet_id
        config.save()

        # FIXME(6): get DMs to me
        return results


twitter = Twitter()


async def poller(telegram):
    """Check twitter to see if something's new."""
    logger.debug("Running twitter poller")
    tweets = await twitter.get()
    for tweet in tweets:
        logger.debug("Poller got tweet: %s", tweet)
        await telegram.update(tweet)


async def go(telegram, init_delay):
    """Set up listener."""
    if init_delay:
        await asyncio.sleep(config.POLLER_DELAY / 2)

    while True:
        await poller(telegram)
        await asyncio.sleep(config.POLLER_DELAY)
