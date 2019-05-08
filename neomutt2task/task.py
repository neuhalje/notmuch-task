import re
from subprocess import call, Popen, PIPE


def rollback():
    print("INFO: Rolling back incomplete task/note creation:")
    call(['task', 'rc.confirmation=off', 'undo'])

res = Popen(['task', 'add', 'pri:L', '+email', '--', message], stdout=PIPE)
match = re.match("^Created task (\d+).*", res.stdout.read())
if match:
    print(match.string.strip())
    id = match.group(1)
    uuid = Popen(['task', id, 'uuids'], stdout=PIPE).stdout.read().strip()
    ret = call(['task', id, 'annotate', '--', 'email:', 'Notes'])
    if ret:
        print("ERR: Sorry, cannot annotate task with ID=%s." % id)
        rollback()

    notes_file = notes_folder + "/" + uuid + ".txt"
    try:
        shutil.copy(tmpfile, notes_file)
        os.remove(tmpfile)
    except:
        print("ERR: Sorry, cannot create notes file \"%s\"." % notes_file)
        rollback()
