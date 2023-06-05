import os


def check_if_exists(object_path):
    found = False

    try:
        os.stat(object_path)
        found = True

    except OSError:
        pass

    return found


def create_dir_if_doesnt_exit(dir_path):
    if not check_if_exists(dir_path):
        os.mkdir(dir_path)