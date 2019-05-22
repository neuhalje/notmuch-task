import os


def get_test_resource_root_dir():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "messages")
    return directory


def get_test_resource_dir(*subdirs):
    directory = os.path.join(get_test_resource_root_dir(), *subdirs)
    return directory


def get_test_resource(*subdirs, filename):
    """
    get_test_resource("dir1"
    :param subdir:
    :param filename:
    :return:
    """
    path = os.path.join(get_test_resource_dir(*subdirs), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return path
