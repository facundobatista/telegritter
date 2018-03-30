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
import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler

from telegritter import telegram, twitter


def exception_handler(exc_type, exc_value, tb):
    """Handle an unhandled exception."""
    exception = traceback.format_exception(exc_type, exc_value, tb)
    logger = logging.getLogger('telegritter')
    logger.error("Unhandled exception!\n%s", "".join(exception))


# set up the logging
logfile = 'telegritter.log'
print("Saving logs to", repr(logfile))
logfolder = os.path.dirname(logfile)
if logfolder and not os.path.exists(logfolder):
    os.makedirs(logfolder)

logger = logging.getLogger('telegritter')
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(logfile, maxBytes=1e6, backupCount=10)
formatter = logging.Formatter("%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# hook the exception handler
sys.excepthook = exception_handler


async def go():
    """Main entry point."""
    telegram.telegram.init()
    twitter.twitter.init()
    await asyncio.gather(
        telegram.go(twitter.twitter, init_delay=False),
        twitter.go(telegram.telegram, init_delay=True),
    )
