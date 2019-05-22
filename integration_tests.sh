#!/usr/bin/env bash

eval $(./tst_setup_env.sh) || { echo Failed to setup ENV; exit 1; }

error_count=0

count_error()
{
  error_count=$(($error_count + 1))
}

notmuchtask()
{
  pipenv run notmuchtask $*
}

test_exitcode()
{
  expected=$1
  test_name="$2"
  echo "$test_name" >&2
  shift
  shift
  echo "Running: $*" >&2
  $*
  actual=$?
  if [ ! $actual -eq $expected ]; then
    echo "FAILED: $test_name: Expected exit code $expected but got $actual" >&2
    count_error
  fi
}

empty()
{
  test_name="$1"
  shift
  if [ ! "$1" = "" ]; then
    echo "FAILED: $test_name: Result should be empty" >&2
    count_error
  fi
}

not_empty()
{
  test_name="$1"
  shift
  if [ "$1" = "" ]; then
    echo "FAILED: $test_name: Result should not be empty" >&2
    count_error
  fi
}

same()
{
  test_name="$1"
  shift
  if [ ! "$1" = "$2" ]; then
    echo "FAILED: $test_name: Expected '$1' actual '$2'" >&2
    count_error
  fi
}

new_test()
{
 echo >&2
 echo ------------------------- $1 >&2
 echo >&2
}

new_test "help"
test_exitcode 0 "help works" notmuchtask --help

new_test "invalid file handling"
test_exitcode 91 "Correct error for invalid file"  notmuchtask find-task /not/existing
test_exitcode 91 "Correct error for invalid file"  notmuchtask find-or-create-task /not/existing

#
# Test some mails that should be parsed
#

while read TEST_MESSAGE
do
       
        new_test "$TEST_MESSAGE"
        
        new_test "mails without tasks"
        taskid=$(test_exitcode 93 "find-task for message without task is empty" notmuchtask find-task $TEST_MESSAGE)
        empty "No taskid returned if no task found" "$taskid"

        new_test "creating tasks is idempotend"
        taskid_created=$(test_exitcode 0 "find-or-create-task for message without task gives id" notmuchtask --debug find-or-create-task $TEST_MESSAGE)
        not_empty "taskid should be returned if task is created" "$taskid_created"

        taskid_found=$(test_exitcode 0 "find-task for message with task is returned" notmuchtask find-task $TEST_MESSAGE)
        same "the same taskid should be returned when searching" $taskid_created $taskid_found

done < <(find $MAILDIR/expected_to_pass -name \*.eml)

#
# Messages that should fail
#

while read TEST_MESSAGE
do
       
        new_test "$TEST_MESSAGE should fail to parse"
        
        taskid=$(test_exitcode 90 "find-task for message $TEST_MESSAGE should fail" notmuchtask find-task $TEST_MESSAGE)
        empty "No taskid returned if no task found" "$taskid"

done < <(find $MAILDIR/expected_to_fail -name \*.eml)

if [ ! $error_count -eq 0 ]; then
  echo "$error_count failed tests"
  exit 1
else
  echo Successfully ran integration test!
fi
