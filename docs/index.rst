.. Connect four documentation master file, created by
   sphinx-quickstart on Thu May 16 09:49:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Connect four's documentation!
========================================
Connect four is a django application, that allows users of your site to play
`connect four game <http://en.wikipedia.org/wiki/Connect_Four>`_.

Features:
 * user can play against computer opponent
 * scalable board size (min, max and default values in :ref:`settings`)
 * scalable number of chips connected for victory (min, max and default values in :ref:`settings`)
 * user can have more games opened
 * game archive

Todo list:
 * hot seat mode (two players on one computer)
 * two users over network
 * history of moves + replay game
 * statistics in user profile
 * users can pick colour of chips

Application is easily integrable to `Mezzanine CMS <http://mezzanine.jupo.org/>`_,
but if You don't want to use it, You can use included :mod:`connect_four.views`
directly.

Installation and configuration is described in following modules.

Contents:

.. toctree::
   :maxdepth: 4

   installation
   settings
   dependencies
   connect_four


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

