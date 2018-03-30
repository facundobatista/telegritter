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

import logging
import os
import pickle

from telegritter.utils import SafeSaver, config_basedir

logger = logging.getLogger(__name__)

FILEPATH = os.path.join(config_basedir, 'telegritter.cfg')


class _Config(object):
    """The configuration."""

    # config options, with their default
    _config_options = {
        'TELEGRAM_LAST_ID': None,
        'TELEGRAM_TOKEN': None,
        'TWITTER_TOKENS': None,
        'USER_ALLOWED': None,
        'POLLER_DELAY': 10,
        'TWITTER_LAST_ID': None,
    }

    def __init__(self):
        self._needs_save = 0

        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            self._data = {}
            return

        with open(FILEPATH, 'rb') as fh:
            self._data = pickle.load(fh)
        logger.debug("Loaded: %s", self._data)

    def __getattr__(self, key):
        return self._data.get(key, self._config_options[key])

    def __setattr__(self, key, value):
        if key in self._config_options:
            if key not in self._data or self._data[key] != value:
                self._data[key] = value
                self._needs_save += 1
        else:
            if key.startswith('_'):
                super().__setattr__(key, value)
            else:
                raise AttributeError

    def save(self):
        """Save the config to disk."""
        if self._needs_save:
            logger.debug("Saving: %s", self._data)
            with SafeSaver(FILEPATH) as fh:
                pickle.dump(self._data, fh)
                self._needs_save = 0


config = _Config()
