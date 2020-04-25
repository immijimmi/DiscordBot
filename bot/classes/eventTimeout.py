from datetime import datetime, timedelta

from ..constants import Defaults

class EventTimeout:
    def __init__(self, key, duration_seconds=Defaults.timeout_duration):
        self.__key = key
        self.__duration = duration_seconds

        self.reset()

    def is_expired(self):
        return (self.__start + timedelta(seconds=self.__duration)) <= datetime.now()

    def reset(self):
        self.__start = datetime.now()
