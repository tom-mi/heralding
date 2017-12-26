# Copyright (C) 2017 Johnny Vestergaard <jkv@unixcluster.dk>
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

import json
import uuid
import logging
from datetime import datetime

import heralding.honeypot
from heralding.reporting.reporting_relay import ReportingRelay

logger = logging.getLogger(__name__)


class Session:
    def __init__(self, source_ip, source_port, protocol, users, destination_port=None, destination_ip=None):

        self.id = uuid.uuid4()
        self.source_ip = source_ip
        self.source_port = source_port
        self.protocol = protocol
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.timestamp = datetime.utcnow()
        self.login_attempts = 0
        self.session_ended = False

        self.connected = True

        # for session specific volatile data (will not get logged)
        self.vdata = {}

        self.last_activity = datetime.utcnow()

    def activity(self):
        self.last_activity = datetime.utcnow()

    def get_number_of_login_attempts(self):
        return self.login_attempts

    def is_connected(self):
        return self.connected

    def add_auth_attempt(self, _type, **kwargs):
        self.login_attempts += 1
        entry = {'timestamp': datetime.utcnow(),
                 'session_id': self.id,
                 'auth_id': uuid.uuid4(),
                 'source_ip': self.source_ip,
                 'source_port': self.source_port,
                 'destination_ip': heralding.honeypot.Honeypot.public_ip,
                 'destination_port': self.destination_port,
                 'protocol': self.protocol,
                 'username': None,
                 'password': None
                 }
        if 'username' in kwargs:
            entry['username'] = kwargs['username']
        if 'password' in kwargs:
            entry['password'] = kwargs['password']

        ReportingRelay.logAuthAttempt(entry)

        self.activity()
        logger.debug('{0} authentication attempt from {1}:{2}. Auth mechanism: {3}, session id {4} '
                     'Credentials: {5}'.format(self.protocol, self.source_ip,
                                               self.source_port, _type, self.id, json.dumps(kwargs)))

    def end_session(self):
        if not self.session_ended:
            self.session_ended = True
            self.connected = False

            entry = {'timestamp': self.timestamp,
                     'duration': (int)((datetime.utcnow() - self.timestamp).total_seconds()),
                     'session_id': self.id,
                     'source_ip': self.source_ip,
                     'source_port': self.source_port,
                     'destination_ip': heralding.honeypot.Honeypot.public_ip,
                     'destination_port': self.destination_port,
                     'protocol': self.protocol,
                     'auth_attempts': self.get_number_of_login_attempts()
                     }

            ReportingRelay.logSessionEnded(entry)
            logger.debug('Session with session id {0} ended'.format(self.id))
