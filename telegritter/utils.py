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

import appdirs
import os


def _ensure_dir_exists(dirpath):
    """If the directory doesn't exist, create it."""
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


# simple attributes to have this calculated at one place only
app = appdirs.AppDirs("telegritter")

# if exists, move the old config file into a new configuration dir.
if not os.path.exists(app.user_config_dir):
    config_file_name = "telegritter.cfg"
    _ensure_dir_exists(app.user_config_dir)
    prev_cfg = os.path.join(os.path.dirname(app.user_config_dir), config_file_name)
    if os.path.exists(prev_cfg):
        os.rename(prev_cfg, os.path.join(app.user_config_dir, config_file_name))
_ensure_dir_exists(app.user_data_dir)
_ensure_dir_exists(app.user_cache_dir)

data_basedir = app.user_data_dir
cache_basedir = app.user_cache_dir
config_basedir = app.user_config_dir


class SafeSaver(object):
    """A safe saver to disk.

    It saves to a .tmp and moves into final destination, and other
    considerations.
    """

    def __init__(self, fname):
        self.fname = fname
        self.tmp = fname + ".tmp"
        self.fh = None

    def __enter__(self):
        self.fh = open(self.tmp, 'wb')
        return self.fh

    def __exit__(self, *exc_data):
        self.fh.close()

        # only move into final destination if all went ok
        if exc_data == (None, None, None):
            if os.path.exists(self.fname):
                # in Windows we need to remove the old file first
                os.remove(self.fname)
            os.rename(self.tmp, self.fname)
