# Copyright 2017 Facundo Batista
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
import json
import logging
from datetime import datetime
from urllib import parse

import aiohttp

from telegritter.config import config

logger = logging.getLogger(__name__)


class Message:
    """The message processed."""

    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_AUDIO = 'audio'

    def __init__(self, message_id, text=None, sent_at=None,
                 extfile_path=None, media_type=None, useful=True):
        self.message_id = message_id
        self.useful = useful
        self.text = text
        self.sent_at = sent_at
        self.extfile_path = extfile_path
        self.media_type = media_type

    @classmethod
    async def _from_update(cls, update):
        """Create from a telegram message."""
        try:
            msg = update['message']
        except KeyError:
            logger.warning("Unknown update type: %r", update)
            return

        # only allow messages from a specific user (set in the first message, can be reset
        # through config)
        from_id = msg['from']['id']
        allowed_user = config.USER_ALLOWED
        if allowed_user is None:
            # user not configured yet, let's set it now
            logger.info("Setting allowed user id to %r", from_id)
            config.USER_ALLOWED = from_id
            config.save()
        else:
            # check user is allowed
            if allowed_user != from_id:
                logger.warning("Ignoring message from user not allowed: %r", from_id)
                return

        if 'text' in msg:
            text = msg['text']
            info = dict(text=text)

        # FIXME: reuse, maybe, for images
        # elif 'photo' in msg:
        #     # grab the content of the biggest photo only
        #     photo = max(msg['photo'], key=lambda photo: photo['width'])
        #     extfile_path = await download_file(photo['file_id'])
        #     media_type = cls.MEDIA_TYPE_IMAGE
        #     text = msg['caption'] if 'caption' in msg else None
        #     info = dict(extfile_path=extfile_path, media_type=media_type, text=text)

        # FIXME: reuse, maybe, for real files (?)
        # elif 'voice' in msg:
        #     # get the audio file
        #     extfile_path = await download_file(msg['voice']['file_id'])
        #     media_type = cls.MEDIA_TYPE_AUDIO
        #     info = dict(extfile_path=extfile_path, media_type=media_type)

        else:
            logger.warning("Message type not supported: %s", msg)
            return

        update_id = int(update['update_id'])
        sent_at = datetime.fromtimestamp(msg['date'])
        return cls(sent_at=sent_at, message_id=update_id, **info)

    @classmethod
    async def from_update(cls, update):
        """Securely parse from update, or return a not useful item."""
        try:
            item = await cls._from_update(update)
        except Exception as exc:
            logger.exception("Problem parsing message from update: %s", exc)
            item = None

        if item is None:
            # bad parsing, crash in _from_update, user not allowed, etc
            update_id = int(update['update_id'])
            item = cls(message_id=update_id, useful=False)
        return item

    def __str__(self):
        return "<Message [{}] {} {!r} ({}, {!r})>".format(
            self.message_id, self.sent_at, self. text, self.media_type, self.extfile_path)


# FIXME: reuse this in a future when we support receiving images from telegram
# API_FILE = "https://api.telegram.org/file/bot{token}/{file_path}"
# def build_fileapi_url(file_path):
#     """Build the proper url to hit the API."""
#     token = config.BOT_AUTH_TOKEN
#     url = API_FILE.format(token=token, file_path=file_path)
#     return url


# FIXME: reuse this in the future when we need real files
# @defer.inline_callbacks
# def download_file(file_id):
#     """Download the file content from Telegram."""
#     url = build_baseapi_url('getFile', file_id=file_id)
#     logger.debug("Getting file path, file_id=%s", file_id)
#     downloader = _Downloader(url)
#     encoded_data = yield downloader.deferred
#
#     logger.debug("getFile response encoded data len=%d", len(encoded_data))
#     data = json.loads(encoded_data.decode('utf8'))
#     if not data.get('ok'):
#         logger.warning("getFile result is not ok: %s", encoded_data)
#         return
#
#     remote_path = data['result']['file_path']
#     url = build_fileapi_url(remote_path)
#    file_path = os.path.join(data_basedir, uuid.uuid4().hex + '-' + os.path.basename(remote_path))
#     logger.debug("Getting file content, storing in %r", file_path)
#     downloader = _Downloader(url, file_path)
#     downloaded_size = yield downloader.deferred
#
#     logger.debug("Downloaded file content, size=%d", downloaded_size)
#     defer.return_value(file_path)


API_BASE = "https://api.telegram.org/bot{token}/{method}"


class Telegram:
    """An interface to Telegram."""

    def init(self):
        """Get tokens from config and start stuff."""
        self.token = config.TELEGRAM_TOKEN
        self.session = aiohttp.ClientSession()

    def _build_get_url(self, method, **kwargs):
        """Build the proper url to hit the API with a GET."""
        url = API_BASE.format(token=self.token, method=method)
        if kwargs:
            url += '?' + parse.urlencode(kwargs)
        return url

    async def update(self, tweet):
        """Send message to Telegram."""
        if not config.USER_ALLOWED:
            logger.warning("Ignoring message (no USER_ALLOWED)")
            return

        print("================== telegram update, user", repr(config.USER_ALLOWED))
        print("================== telegram update, tweet", tweet)
        message = tweet.text  # FIXME build nicier
        kwargs = {
            'chat_id': config.USER_ALLOWED,
            'text': message,
        }
        url = self._build_get_url('sendMessage', **kwargs)
        logger.debug("Sending message, kwargs=%s", kwargs)

        async with self.session.get(url) as resp:
            print("=========== resp, status", resp.status)
            raw_data = await resp.text()

        print("============ resp, raw", repr(raw_data))
        data = json.loads(raw_data)
        if data['ok']:
            logger.debug("Update ok")
        else:
            logger.error("Update error: %s", data['result'])

    async def get(self):
        """Get messages from Telegram."""
        kwargs = {}
        if config.TELEGRAM_LAST_ID is not None:
            kwargs['offset'] = config.TELEGRAM_LAST_ID + 1
        url = self._build_get_url('getUpdates', **kwargs)
        logger.debug("Getting updates, kwargs=%s", kwargs)
        # FIXME: support receiving image(s) and sending them to twitter

        # FIXME: recognize that the message is a reply to a previous one, so build that as a
        # reply in twitter (to a normal message, or a DM)

        try:
            async with self.session.get(url) as resp:
                print("=========== resp, status", resp.status)
                raw_data = await resp.text()
        except aiohttp.client_exceptions.ClientConnectorError as exc:
            logger.error("AIOHTTP error: %s", exc)
            return []

        print("============ resp, content", repr(raw_data))
        logger.debug("Process encoded data len=%d", len(raw_data))
        data = json.loads(raw_data)
        messages = []
        if data.get('ok'):
            results = data['result']
            logger.debug("Telegram results ok! len=%d", len(results))
            msg = None
            for item in results:
                logger.debug("Processing result: %s", item)
                msg = await Message.from_update(item)
                print("====== parsed", msg, msg.useful)
                if msg.useful:
                    messages.append(msg)
            if msg is not None:
                config.TELEGRAM_LAST_ID = msg.message_id
                config.save()
        else:
            logger.warning("Telegram result is not ok: %s", data)
        return messages


telegram = Telegram()


async def poller(twitter):
    """Check telegram to see if something's new."""
    logger.debug("Running telegram poller")
    messages = await telegram.get()
    for message in messages:
        logger.debug("Poller got message: %s", message)
        twitter.update(message.text)


async def go(twitter, init_delay):
    """Set up listener."""
    if init_delay:
        await asyncio.sleep(config.POLLER_DELAY / 2)

    while True:
        await poller(twitter)
        await asyncio.sleep(config.POLLER_DELAY)
