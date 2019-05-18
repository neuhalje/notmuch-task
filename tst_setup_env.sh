#!/usr/bin/env sh

#
# Create a completely new setup (Maildir, notmuch DB, pipenv)
#


get_exec()
{
   query=$1
   cmd=$(which $query)
   if [ "$cmd" = "" ]; then
     echo "'$query' not in path; aborting" >&2
     exit 1
   fi

   if [ ! -x $cmd ]; then
     echo "'$cmd' not an executable; aborting" >&2
     exit 1
   fi
   echo "Using '$cmd' for '$query'" >&2
   echo $cmd
}

notmuch=$(get_exec "notmuch") || exit 1
task=$(get_exec "task") || exit 1
pipenv=$(get_exec "pipenv") || exit 1
mktemp=$(get_exec "mktemp") || exit 1

#
# Setup
#


temp_dir=$($mktemp -d)  || { echo failed to create temp. dir; exit 1; }

echo Using $temp_dir >&2

export MAILDIR="${temp_dir}/Mail"
echo Using MAILDIR $MAILDIR >&2 
mkdir -p "$MAILDIR" || { echo failed to create mail dir $MAILDIR; exit 1; }

export NOTMUCH_CONFIG="${temp_dir}/notmuch-config"
echo Using NOTMUCH_CONFIG $NOTMUCH_CONFIG >&2 

cat <<EOF>"${NOTMUCH_CONFIG}"
# .notmuch-config - Configuration file for the notmuch mail system
[database]
path=${MAILDIR}

[user]
name=Example User
primary_email=recipent@localhost

[new]
tags=new
ignore=.mbsyncstate;.isyncuidmap.db;.uidvalidity

[search]
exclude_tags=deleted;spam;muted

[maildir]
synchronize_flags=true
EOF

cp -r test/example-mails/* "$MAILDIR" || { echo Failed to copy mails to $MAILDIR; exit 1; }

$notmuch new  >&2 || { echo notmuch new failed; exit 1; }

msg_count=0$($notmuch count "Example Message")
if [ ! $msg_count -gt 0 ]; then
  echo "Should have found messages - aborting" >&2
  exit 1
fi

#
# Taskwarrior
#


export TASKRC="${temp_dir}/taskrc"
export TASK_DATA="${temp_dir}/tasks"
mkdir -p "$TASK_DATA" || { echo failed to create $TASK_DATA; exit 1; }

cat <<EOF>"${TASKRC}"
data.location=$TASK_DATA
EOF

task_count=0$($task count)
if [ ! $task_count -eq 0 ]; then
  echo "Should have found no tasks - aborting" >&2
  exit 1
fi

#
# Install
#

export WORKON_HOME="${temp_dir}/venv"
mkdir -p "$WORKON_HOME" || { echo failed to create $WORKON_HOME; exit 1; }
$pipenv --three --site-packages >&2 || { echo failed to create venv ; exit 1; }
$pipenv run python --version >&2
$pipenv run pip --version >&2
$pipenv run pip install  --editable .  >&2 || { echo failed to install from source; exit 1; }

# eval this
echo export WORKON_HOME=$WORKON_HOME
echo export MAILDIR=$MAILDIR
echo export NOTMUCH_CONFIG=$NOTMUCH_CONFIG
echo export TASKRC=$TASKRC
