mail to taskwarrior
#######################

.. image:: https://travis-ci.org/neuhalje/notmuch-task.svg?branch=master
    :target: https://travis-ci.org/neuhalje/notmuch-task

Linking mails (mutt, neomutt) to taskwarrior tasks and the other way around by utilising notmuch.

- Create tasks from (neo)mutt with one command
- Find tasks already assigned to e-mails


Installing
**************

``pip install notmuchtask``


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

Exit codes
-----------

0
  Command ran successfully. The task-id has been written to stdout
90
  An unexpected error has occured
91
  File not found. The file passed could not be opened
92
  The message(-id) could not be found in notmuch
93
  The task could not be found

Creating tasks
===============

The ``find-or-create-task`` command will find the task(s) assigned to a
 message and will create a new task if needed.

.. code:: shell

  # reading the message from stdin
  cat test.eml|notmuchtask  find-or-create-task
  # the first time a new task is created with the subject as title
  99c0768c-2dbd-4c8b-9b74-afe610653dd1

  cat test.eml|notmuchtask  find-or-create-task
  # the second time no new task is created
  99c0768c-2dbd-4c8b-9b74-afe610653dd1

  # or reading the message by path
  notmuchtask  find-or-create-task test.eml
  99c0768c-2dbd-4c8b-9b74-afe610653dd1


Exit codes
-----------

0
  Command ran successfully. The task-id has been written to stdout
90
  An unexpected error has occurred
91
  File not found. The file passed could not be opened
92
  The message(-id) could not be found in notmuch

(neo)mutt
**************

Add this to your ``.muttrc``:

.. code:: text

  # Make sure that there are no spaces at the beginning of the line
  macro index,pager <F8> \
  "<enter-command>set my_old_pipe_decode=\$pipe_decode my_old_wait_key=\$wait_key nopipe_decode nowait_key<enter>\
  <pipe-message>notmuchtask --debug find-or-create-task<enter>\
  <enter-command>set pipe_decode=\$my_old_pipe_decode wait_key=\$my_old_wait_key<enter>" \
  "notmuchtask: assign mail to a task"



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

Develop
=============

Tidbits about development.

Run DEV version
****************

For testing purposes you can run the code directly from the repository:

.. code:: shell

  # Setup the virtual environment
  # Install site package with python3 bindings for notmuch
  apt install python3-notmuch
  pipenv --rm  # just in case
  pipenv --python 3.6 --site-packages
  pipenv install --dev

.. code:: shell

  # run the code
  pipenv shell
  pip install --editable .

  notmuchtask --help

TODOs
****************

Known Bugs
============

* Mails with non-utf-8 charset fail to parse
* Messages without subject fail to parse

Ideas
============

Prio A (must), B (should), C (maybe never .. )

* (A) Passthrough commands: enter the command for the task for a mail
* (A) Edit task description on creation
* (B) Use taskwarriors UDAs to store the message ID
* (B) Transaction with task and notmuch incl. locking
* (C) Virtual folder to include tasks in mutt (??) (FUSE?)
