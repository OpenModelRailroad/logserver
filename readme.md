# OMRR Logserver and UI

## Requirements

* Virtualenv - https://virtualenv.pypa.io/en/latest/
* pip - https://pip.pypa.io/en/stable/
* Python 3.7 - https://www.python.org/

## Install

1. Clone the repository
2. cd into directory
3. Create a virtualenvironment with ````virtualenv venv````
4. Activate virtualenv with (macOS / Linux) ```source venv/bin/activate```
5. Install all requirements from file with ```pip install -r requirements.txt```
6. Migrate Database with ```python manage.py migrate```
7. Start the server with ```python manage.py runserver```

On *nix: Alternative you can run the install script in /scripts. (needs sudo or ```chmod u+x ./scripts/*.sh```)

## Testing Sniffer connecting
**!!! requires nc installed (https://www.ionos.com/digitalguide/server/tools/netcat/) or (https://www.npmjs.com/package/node-netcat)!!!**
* Check if the message "waiting for sniffers on <host>:<port>" appears.
* connect to the logserver with ````nc -u -v localhost 11337```` (check for IP and Port if changed in settings.py)
* send a message ```{'type': 'heartbeat', 'ip': '192.168.1.1', 'mac': '24:4b:fe:b9:b9:9e','hostname': 'cli'}```

## To be considered
* https://django-split-settings.readthedocs.io/en/latest/
* https://stackoverflow.com/questions/50198741/django-influxdb
* https://django-q.readthedocs.io/en/latest/architecture.html
* https://github.com/Koed00/django-q/issues/367

## License
see license.md