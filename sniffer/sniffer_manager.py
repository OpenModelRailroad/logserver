from datetime import datetime, timedelta
import logging
import time
from dateutil import tz


def check_active_sniffer():
    from railmessages.models import RawMessage
    from .models import Sniffer
    logger = logging.getLogger(__name__)
    from django.conf import settings

    while True:
        sniffers = Sniffer.objects.all()
        sniffer_ids = []
        for sniffer in sniffers:
            django_tz = tz.gettz(settings.TIME_ZONE)
            now = datetime.now(django_tz)
            delta = now - sniffer.last_connection
            delta_seconds = delta.total_seconds()

            if settings.DEBUG:
                print("Checking Sniffer =============================================================================")
                print(sniffer.hostname)
                print(sniffer.last_connection)
                print(type(sniffer.last_connection))
                print(delta)
                print(delta_seconds)
                print("==============================================================================================")

            # if delta between two heartbeats is greather than 20 seconds, 2 heartbeats are missed
            if delta_seconds > 20.0:
                sniffer.is_connected = False
                sniffer.last_connection = datetime.date(datetime.now())
                print("Sniffer %s no longer connected" % sniffer.hostname)
            else:
                sniffer.is_connected = True
                sniffer.last_connection = datetime.date(datetime.now())
                print("Sniffer %s connected" % sniffer.hostname)
            sniffer.save()

        time.sleep(10)
