django-connect-four
===================

Django application, that allows users of your site to play
`connect four game <http://en.wikipedia.org/wiki/Connect_Four>`_.

Features:
 * user can play against computer opponent
 * scalable board size (min, max and default values)
 * scalable number of chips connected for victory (min, max and default values)
 * user can have more games opened
 * game archive

Todo list:
 * hot seat mode (two players on one computer)
 * two users over network
 * history of moves + replay game
 * statistics in user profile
 * users can pick colour of chips

Application is easily integrable to `Mezzanine CMS <http://mezzanine.jupo.org/>`_,
but if You don't want to use it, You can use included views directly.

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

