# Intro

This is a Django app for advanced polling. Will hopefully be fun :)

# Setup Guide

- Install Python 3.6+
- Create a new virtual environment and source it (I like to use virtualenvwrapper)
- run `pip install -r requirements.txt`
- Create a file `poll/app_secrets.py` and ask Arya for the contents.
- Run `python test_setup_script.py` - it should print out a large JSON at the end.
- Run `python manage.py test polls` - make sure all tests pass.
- Run `python manage.py runserver` to run the test local instance.

