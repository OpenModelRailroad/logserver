#!/bin/bash
#-- Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent
#--
#-- This file is part of "OMRR".
#--
#-- "OMRR" is free software: you can redistribute it and/or modify
#-- it under the terms of the GNU General Public License as published by
#-- the Free Software Foundation, either version 3 of the License, or
#-- (at your option) any later version.
#--
#-- "OMRR" is distributed in the hope that it will be useful,
#-- but WITHOUT ANY WARRANTY; without even the implied warranty of
#-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#-- GNU General Public License for more details.
#--
#-- You should have received a copy of the GNU General Public License
#-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

#-- Install Script for OMRR Logserver

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
} >>.env

#-- install all python packages
pip install -r requirements.txt

#-- initial migrate of database
python manage.py migrate
