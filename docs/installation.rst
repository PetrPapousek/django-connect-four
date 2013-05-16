Installation
============

Get a fresh clone from repository::

   git clone git@github.com:PetrPapousek/django-connect-four.git

and place it to Your Python path.

Add connect four (and dependencies) to your Installed apps::

    ...
    "mezzanine.core",
    "dajaxice",
    "json_field",
    "crispy_forms",
    "connect_four",
    ...

Activate your virtualenv and install requirements from file requirements.txt, for example by:

    pip install -r connect_four/requirements.txt

Run syncdb::

    python manage.py syncdb

