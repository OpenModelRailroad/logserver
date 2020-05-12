#!/bin/bash

#-- Install Script for OMRR Logserver ONLY FOR DEVELOPMENT PURPOSES

DIR='./venv'

cd ..

if [[ ! -d "$DIR" ]]; then
  virtualenv venv
fi

deactivate
source venv/bin/activate


pip install -r requirements.txt
python manage.py migrate

./scripts/run.sh