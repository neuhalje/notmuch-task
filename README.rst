#######################
neomutt to taskwarrior
#######################

Linking mails (mutt, neomutt) to taskwarrior tasks and the other way around by utilising notmuch.

- Create tasks from (neo)mutt with one command
- Find tasks already assigned to e-mails


**************
Installing
**************

TODO!


=============
Usage
=============

``notmuchtask`` links e-mails to tasks in taskwarrior. This is done by assigning notmuch tags to the e-mails.

cli
**************

Finding tasks
===============

The ``find-task`` command will find the task(s) assigned to a message

.. code:: shell

  # reading the message from stdin
  cat test.eml|notmuchtask  find-task
  99c0768c-2dbd-4c8b-9b74-afe610653dd1

  # or reading the message by path
  notmuchtask  find-task test.eml


(neo)mutt
**************

Add this to your ``.muttrc``:

.. code:: text

  macro index,pager t "<pipe-message>mutt2task.py<enter>


configuring
*************

notmuchtask can be configured by a config file:

.. code:: ini

  [tags]
  # notmuchtask uses notmuch tags to link messages to tasks
  # `prefix` is used as a prefix to the taskid. E.g.
  # if prefix is set to 'taskid:', and the task
  # e1544da8-8b9b-4bda-b4bc-8642c5627b59 is linked to the message
  # the tag 'taskid:e1544da8-8b9b-4bda-b4bc-8642c5627b59' is set on the
  # message.
  # default: taskid:
  prefix = taskid:

  [taskwarrior]
  # Executable
  #
  executable = task

The following config files are evaluated, the first found configfile is used:

#. The file passed with ``--configfile``

#. The file pointed to by the environment variable ``NOTMUCHTASKRC``

#.  ``~/.notmuchtask.conf``

=============
Develop
=============

****************
Run DEV version
****************

.. code:: shell 
  # Setup the virtual environment
  # Install site package with python3 bindings for notmuch
  apt install python3-notmuch
  pipenv --python 3.6 --site-packages

.. code:: shell 
  # run the code
  pipenv shell
  pip install --editable .

  notmuchtask --help

****************
TODOs
****************

* Transaction with task and notmuch incl. locking
