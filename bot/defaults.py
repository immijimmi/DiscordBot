from .classes.timeoutDuration import TimeoutDuration
from .classes.permissions import Permissions

class Defaults:
    state_filename = "data.json"

    timeout_duration = TimeoutDuration(1)

    permissions = Permissions(Permissions.levels["none"], [])