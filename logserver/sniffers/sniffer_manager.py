from datetime import datetime, timedelta
import logging
import time
from dateutil import tz
from sniffer.models import Sniffer
from django.conf import settings

logger = logging.getLogger("logserver")


def check_active_sniffer():
    while True:
        sniffers = Sniffer.objects.all()
        for sniffer in sniffers:
            django_tz = tz.gettz(settings.TIME_ZONE)
            now = datetime.now(django_tz)
            delta = now - sniffer.last_connection
            delta_seconds = delta.total_seconds()

            if settings.DEBUG:
                logger.info(
                    "Checking Sniffer =============================================================================")
                logger.info("Hostname %s " % sniffer.hostname)
                logger.info("Last Connection Time: %s" % sniffer.last_connection)
                logger.info("time delta: %s" % delta)
                logger.info("delta_seconds: %s" % delta_seconds)
                logger.info("Connected: %s" % sniffer.is_connected)
                logger.info(
                    "==============================================================================================")

            # if delta between two heartbeats is greather than 20 seconds, 2 heartbeats are missed
            if delta_seconds >= 60.0:
                sniffer.is_connected = False
                sniffer.save()
                try:
                    sniffer.delete()
                    logger.info("Removed Sniffer")
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

        time.sleep(10)
