import logging
import subprocess


class Task(object):
    def __init__(self, task_id, message_id, subject):
        self.task_id = task_id
        self.message_id = message_id
        self.subject = subject

    @staticmethod
    def new_task(message_id, subject):
        return Task(task_id=None, message_id=message_id, subject=subject)


class Taskwarrior(object):
    def __init__(self, tw_executable):
        self.tw_executable = tw_executable
        import sys
        self._subprocess_has_encoding = sys.version_info.minor >= 6

    def add(self, subject):
        self._task("add", subject)
        # https://taskwarrior.org/support/faq.html#q16
        task_id = self._task("+LATEST", "uuids").rstrip()
        return task_id

    def annotate(self, task_id, annotation):
        self._task("annotate", task_id, annotation)

    def _task(self, *args):
        cmd = [self.tw_executable, *args]
        logging.debug("Executing {}".format(cmd))

        if self._subprocess_has_encoding:
            # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
            res = subprocess.run(cmd, encoding="utf-8", stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout = res.stdout
        else:
            # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
            res = subprocess.run(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout = res.stdout.decode("utf-8")
        if res.returncode != 0:
            logging.error(res.stderr)
            raise Exception("Error running {}".format(' '.join(cmd)))
        return str(stdout)

    def rollback(self):
        self._task(['rc.confirmation=off', 'undo'])


class Repository(object):
    """
    Adapter around taskwarrior
    """

    def __init__(self, tw: Taskwarrior):
        self.tw = tw

    def __enter__(self):
        """
        Implements the context manager protocol.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Implements the context manager protocol.
        """
        # TODO: Implement
        pass

    def create_task(self, task: Task) -> Task:
        """
        Create the task in taskwarrior, return persisted task
        :param task:
        :return:
        """
        task_id = self.tw.add(task.subject)
        task.task_id = task_id

        self.tw.annotate(task_id,
                         "Imported from message {}".format(task.message_id))
        # TODO: add UDA
        # FIXME: load from repo
        return task
