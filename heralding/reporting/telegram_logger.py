# Copyright (C) 2017 Thomas Reifenberger <tom-mi at rfnbrgr.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from heralding.reporting.base_logger import BaseLogger
import urllib.request

logger = logging.getLogger(__name__)


class TelegramLogger(BaseLogger):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id
        logger.info('Telegram logger started.')

    def handle_log_data(self, data):
        message = (
            "*Honeypot Alert - {protocol}* \n"
            "Authentication attempt from {source_ip}:{source_port} "
            "with username {username} and password {password}"
            ).format(**data)

        url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=self.token)
        params = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }
        encoded_params = urllib.parse.urlencode(params)
        urllib.request.urlopen(url + '?' + encoded_params)
