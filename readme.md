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