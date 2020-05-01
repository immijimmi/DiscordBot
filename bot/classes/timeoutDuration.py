class TimeoutDuration:
    def __init__(self, seconds):
        if seconds <= 0:
            raise ValueError("Timeout duration must be a positive non-zero value. {0} seconds is not valid".format(seconds))

        self._seconds = seconds

    @property
    def seconds(self):
        return self._seconds

    def to_user_string(self):
        seconds = self.seconds

        minutes = int(seconds/60)
        seconds -= minutes*60

        hours = int(minutes/60)
        minutes -= hours*60

        days = int(hours/24)
        hours -= days*24

        segment_lookup = {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
        segments = [
            "{0} {1}".format(segment_lookup[segment_key], segment_key)
            for segment_key in ("days", "hours", "minutes", "seconds")
            if segment_lookup[segment_key] > 0
            ]

        return ", ".join(segments)

    @staticmethod
    def from_user_string(string):
        pass  ##### TODO