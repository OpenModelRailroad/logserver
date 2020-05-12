#!/bin/bash

#-- Install Script for OMRR Logserver ONLY FOR DEVELOPMENT PURPOSES

DIR='./venv'
#-- Go back one directory
cd ..

#-- Check if Virtualenv created
if [[ ! -d "$DIR" ]]; then
  virtualenv venv
fi

#-- Activate virtualenv
deactivate
source venv/bin/activate

#-- Create a default .env file
{
  echo 'SECRET_KEY=lwkjefh9382dino9hc3+*2b23423(2'
  echo 'DEBUG=True'
  echo 'DATABASE_URL=sqlite://./db.sqlite3'
  echo 'ALLOWED_HOSTS=.localhost, 127.0.0.1'
} >> .env

#-- install all python packages
pip install -r requirements.txt

#-- initial migrate of database
python manage.py migrate

#-- Start the server
./scripts/run.sh
