# OMRR Logserver and UI

## Requirements
* Virtualenv - https://virtualenv.pypa.io/en/latest/
* Python 3.8 - https://www.python.org/

## Install
1. Clone the repository
2. cd into directory 
3. Create a virtualenvironment with ````virtualenv venv````
4. Activate virtualenv with (macOS / Linux) ```source venv/bin/activate```
5. Install all requirements from file with ```pip install -r requirements.txt```
6. Migrate Database with ```python manage.py migrate```
7. Start the server with ```python manage.py runserver```

Alternative you can run the install script in /scripts. (needs sudo or ```chmod u+x ./scripts/*.sh```)

## Testing Sniffer connecting
* Check if the message "waiting for sniffers on <host>:<port>" appears.  
* connect to the logserver with ````nc -v <host> <port>````
* send a message ```{'ip':'127.0.0.1', 'mac': '00:80:41:ae:fd:7f', 'hostname': 'block_01'}```


## Docker integration (not finished implemented)
You can use the docker integration. Just run ```docker-compose up```  

## To be considered
* https://django-split-settings.readthedocs.io/en/latest/
* InfluxDB QL
* https://stackoverflow.com/questions/50198741/django-influxdb
* https://django-q.readthedocs.io/en/latest/architecture.html