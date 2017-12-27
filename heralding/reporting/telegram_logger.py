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

import asyncio
from collections import deque
from heralding.reporting.base_logger import BaseLogger
import heralding.misc.common as common
import logging
import urllib.request

logger = logging.getLogger(__name__)


class TelegramLogger(BaseLogger):
    def __init__(self, loop, token, chat_id, digest_interval_seconds=60, digest_detail_messages=3):
        super().__init__()
        self.loop = loop
        self.token = token
        self.chat_id = chat_id
        self.digest_interval_seconds = digest_interval_seconds
        self.detail_messages = deque(maxlen=digest_detail_messages)
        self.stats = {}
        logger.info('Telegram logger started.')

    def start(self):
        self.telegram_sender_task = self.loop.create_task(self.start_digest_sender())
        self.telegram_sender_task.add_done_callback(common.on_unhandled_task_exception)
        super().start()

    async def start_digest_sender(self):
        while self.enabled:
            await asyncio.sleep(self.digest_interval_seconds)
            self.send_alert_digest()

    def send_alert_digest(self):
        if not self.stats:
            return
        message = '*Honeypot Alert*\n'

        for protocol in sorted(self.stats):
            message += '{} {} authentication attempts\n'.format(self.stats[protocol], protocol)

        message += '\nLatest {} attempts:\n'.format(len(self.detail_messages))
        for detail_message in self.detail_messages:
            message += detail_message

        self.send_telegram_message(message)
        self.stats.clear()
        self.detail_messages.clear()

    def send_telegram_message(self, message):
        url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=self.token)
        params = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }
        encoded_params = urllib.parse.urlencode(params)
        urllib.request.urlopen(url + '?' + encoded_params)

    def handle_log_data(self, data):
        message = "{source_ip} -> {protocol} ({username}, {password})\n".format(**data)
        self.detail_messages.append(message)

        protocol = data['protocol']
        if protocol not in self.stats:
            self.stats[protocol] = 0
        self.stats[protocol] += 1

    def loggerStopped(self):
        # send final digest to handle leftover messages
        self.send_alert_digest()
