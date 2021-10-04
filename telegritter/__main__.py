# Copyright 2021 Facundo Batista
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

"""Run the 'telegritter' daemon."""

import argparse
import asyncio

import infoauth

from telegritter import main
from telegritter.twitter import Twitter
from telegritter.telegram import Telegram

parser = argparse.ArgumentParser()
parser.add_argument(
    "telegram_auth_filepath", metavar="telegram-auth-filepath",
    help="The file with Telegram auth info (saved with 'infoauth')")
parser.add_argument(
    "twitter_auth_filepath", metavar="twitter-auth-filepath",
    help="The file with Twitter auth info (saved with 'infoauth')")
args = parser.parse_args()

# load and validate configs
telegram_auth = infoauth.load(args.telegram_auth_filepath)
missing = set(Telegram.AUTH_KEYS) - set(telegram_auth.keys())
if missing:
    print("Error: missing config keys in the Telegram auth file:", missing)
    exit()
twitter_auth = infoauth.load(args.twitter_auth_filepath)
missing = set(Twitter.AUTH_KEYS) - set(twitter_auth.keys())
if missing:
    print("Error: missing config keys in the Twitter auth file:", missing)
    exit()

# start everything
twitter = Twitter(twitter_auth)
telegram = Telegram(telegram_auth)
loop = asyncio.get_event_loop()
loop.run_until_complete(main.main(twitter, telegram))
loop.close()
