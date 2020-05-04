from datetime import datetime, timedelta

from .timeoutDuration import TimeoutDuration

class EventTimeout:  # Single-use timeout objects
    def __init__(self, key, timeout_duration):
        if type(timeout_duration) is not TimeoutDuration:
            raise TypeError(type(timeout_duration))

        self._key = key
        self._duration = timeout_duration
        self._start = datetime.now()

    @property
    def start(self):
        return self._start

    def is_expired(self):
        return (self._start + timedelta(seconds=self._duration.seconds)) <= datetime.now()
