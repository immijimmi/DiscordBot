class TimeoutDuration:
    max_seconds = 86400

    def __init__(self, seconds):
        if seconds <= 0 or seconds > TimeoutDuration.max_seconds:
            raise ValueError("Timeout duration must be a value between 1 and {0} seconds. {1} seconds is not valid".format(TimeoutDuration.max_seconds, seconds))

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
            "{0} {1}{2}".format(segment_lookup[segment_key], segment_key[:-1], "" if segment_lookup[segment_key] == 1 else "s")
            for segment_key in ("days", "hours", "minutes", "seconds")
            if segment_lookup[segment_key] > 0
            ]

        return ", ".join(segments)

    @staticmethod
    def from_user_string(string):
        if string.isdigit():
            return TimeoutDuration(int(string))

        # More parsing approaches should be added as necessary
        
        raise ValueError("Unable to convert to TimeoutDuration: {0}".format(string))
        
