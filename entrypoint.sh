#!/bin/bash

cd project_time_tracker

python manage.py migrate

python manage.py mock_users_and_projects

python manage.py runserver 0.0.0.0:7777