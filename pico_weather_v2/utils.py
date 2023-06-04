import os


def check_if_exists(object_path):
    found = False

    try:
        os.stat(object_path)
        found = True

    except OSError:
        pass

    return found
