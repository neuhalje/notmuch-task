neomutt to taskwarrior
=================================

Linking mails (mutt, neomutt) to taskwarrior tasks and the other way around.

Installing
------------

TODO!

1. Install site package with python3 bindings for notmuch (apt install python3-notmuch)
2. ``pipenv --python 3.6 --site-packages``

Usage
------------

Add this to your ``.muttrc``::

  macro index,pager t "<pipe-message>mutt2task.py<enter>

Develop
=============

TODOs
------

* Transaction with task and notmuch incl. locking