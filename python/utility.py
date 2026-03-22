import datetime
import os


class MSCPException(Exception):
    def __init__(self, message):
        super().__init__(message)


eps = 1e-6


def get_current_timestamp() -> str:
    now = datetime.datetime.now()
    return now.strftime("%b_%d_%H_%M_%S_%Y")


def folder_exists(dir_name: str) -> bool:
    return os.path.isdir(dir_name)
