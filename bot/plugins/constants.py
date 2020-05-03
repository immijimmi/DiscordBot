from ..classes.timeoutDuration import TimeoutDuration

class MessageFormats:
    cannot_find_user_identifier = "Unable to find a user based on the name: `{0}`"
    cannot_parse_timeout_string = "Unable to get a timeout duration from the provided value: `{0}`\nTimeout duration must be a number of seconds between 1 and " + str(TimeoutDuration.max_seconds) + "."
    invalid_arguments = "Invalid command arguments: `{0}`"

    toggle_change_strings = ["toggle"]
    toggle_on_strings = ["on", "enable", "enabled"]
    toggle_off_strings = ["off", "disable", "disabled"]

    list_item = "**{0}**"

class Arguments:
    nickname_separator = " as: "