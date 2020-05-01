from datetime import datetime, timedelta

class EventTimeout:
    def __init__(self, key, timeout_duration):
        self.__key = key
        self.__duration = timeout_duration  # Should be an instance of TimeoutDuration class

        self.reset()

    def is_expired(self):
        return (self.__start + timedelta(seconds=self.__duration.seconds)) <= datetime.now()

    def reset(self):
        self.__start = datetime.now()
