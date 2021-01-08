"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import time
import threading
from datetime import datetime

from dateutil import tz
from django.conf import settings

from sniffer.models import Sniffer

logger = logging.getLogger("logserver")


class SnifferManager(threading.Thread):

    def __init__(self, name=settings.SNIFFER_MANAGER_THREAD_NAME):
        self._stopevent = threading.Event()
        self._sleepperiod = 10.0
        threading.Thread.__init__(self, name=name)

    def run(self):
        while not self._stopevent.isSet():
            sniffers = Sniffer.objects.all()
            for sniffer in sniffers:
                django_tz = tz.gettz(settings.TIME_ZONE)
                now = datetime.now(django_tz)
                delta = now - sniffer.last_connection
                delta_seconds = delta.total_seconds()

                logger.debug("==============================================================================================")
                logger.debug("Checking Sniffer")
                logger.debug("Hostname %s " % sniffer.hostname)
                logger.debug("Last Connection Time: %s" % sniffer.last_connection)
                logger.debug("time delta: %s" % delta)
                logger.debug("delta_seconds: %s" % delta_seconds)
                logger.debug("Connected: %s" % sniffer.is_connected)
                logger.debug("==============================================================================================")

                # if delta between two heartbeats is greather than 20 seconds, 2 heartbeats are missed
                if delta_seconds >= 60.0:
                    sniffer.is_connected = False
                    sniffer.save()
                    try:
                        sniffer.delete()
                        logger.info("Removed Sniffer %s because of inactivity" % sniffer.hostname)
                    except Exception as e:
                        logger.error("Cannot remove not connected sniffer %s: %s" % (sniffer.hostname, e))
                if 11.0 < delta_seconds < (settings.SNIFFER_MISSED_HEARTBEATS * 10.0):
                    sniffer.is_connected = False
                    sniffer.save()
                    logger.info("Sniffer %s no longer connected" % sniffer.hostname)
                elif delta_seconds < 11.0:
                    sniffer.is_connected = True
                    sniffer.save()
                    logger.info("Sniffer %s connected" % sniffer.hostname)

            self._stopevent.wait(self._sleepperiod)

    def join(self, timeout=None):
        self._stopevent.set()
        logger.info("Set Stop Event %s" % self._stopevent)
        threading.Thread.join(self, 5)
        raise StopIteration
