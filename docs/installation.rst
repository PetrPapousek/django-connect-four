Installation
============

Installation can be done by::

    # Get a fresh clone from repo
    git clone git@github.com:PetrPapousek/django-connect-four.git

    # Activate your virtualenv and install package, for example by::
    virtualenv connect_four_virtualenv
    source connect_four_virtualenv/bin/activate
    cd django-connect-four
    python setup.py install

    # Install requirements from file requirements.txt, for example by:
    pip install -r requirements.txt

Add connect four (and dependencies) to your Installed apps::

    ...
    "mezzanine.core",
    "dajaxice",
    "json_field",
    "crispy_forms",
    "connect_four",
    ...

Run syncdb::

    python manage.py syncdb

