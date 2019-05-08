#!/usr/bin/env sh
export PIPENV_VENV_IN_PROJECT=true
# make install
if [ "x$1" = "x-profile" ]; then
 PROFILE="-m cProfile"
 shift
fi


# Prevent globbing; allow to pass --cors '*'
set -f
pipenv  run  python $PROFILE neomutt2task/__main__.py $*
