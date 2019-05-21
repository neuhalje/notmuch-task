import os


def get_test_resource_root_dir():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "messages")
    return directory


def get_test_resource_dir(subdir):
    directory = os.path.join(get_test_resource_root_dir(), subdir)
    return directory


def get_test_resource(subdir, filename):
    path = os.path.join(get_test_resource_dir(subdir), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return path
