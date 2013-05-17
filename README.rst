`Documentation available at Read the Docs. <http://http://django-connect-four.readthedocs.org/>`_

django-connect-four
===================

Django application, that allows users of your site to play
`connect four game <http://en.wikipedia.org/wiki/Connect_Four>`_.

Features:
 * user can play against computer opponent
 * two people can play against each other on same computer
 * both registered and unregistered users can play
 * scalable board size (min, max and default values)
 * scalable number of chips connected for victory (min, max and default values)
 * user can have more games opened
 * game archive

Todo list:
 * two users over network
 * history of moves + replay game
 * statistics in user profile
 * users can pick colour of chips

Application is easily integrable to `Mezzanine CMS <http://mezzanine.jupo.org/>`_,
just set the slug of page where You want to have game running ``new-game``, ``game`` and
``game-archive`` (if You want different slugs, see Configuration doc page).

If You don't want to use Mezzanine, You can use included views directly.

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

