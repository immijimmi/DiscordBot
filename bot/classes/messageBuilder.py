from collections import deque

from .defaults import Defaults

class MessageBuilder:
    discord_message_character_limit = 2000

    def __init__(self, recipients=[], delimiter=Defaults.message_delimiter):
        self._before = deque()
        self._main = deque()
        self._after = deque()

        self._callbacks = []

        self.recipients = list(recipients)
        self.delimiter = delimiter

        self.title = None
        self.mark = Defaults.message_mark

    def __bool__(self):
        return bool(self._main)  # If main is empty the message should be considered empty

    def add(self, item, to_end=True):
        if to_end:
            self._main.append(item)

        else:
            self._main.appendleft(item)

    def surround(self, item, inner=True, mirrored=True):
        if inner:
            self._before.append(item)
            self._after.appendleft(item[::-1] if mirrored else item)

        else:
            self._before.appendleft(item)
            self._after.append(item[::-1] if mirrored else item)

    def add_callback(self, callback):  # Callback methods will recieve a single argument, the message object returned by Discord
        self._callbacks.append(callback)

    def get(self):
        """
        Will return a list of split-up messages if the total message length is above the character limit
        Callbacks will be called with each of the split-up messages separately
        """
        if self:
            full = self.mark + self.delimiter.join(self._before + deque([self.title] if self.title is not None else []) + self._main + self._after)
            
            if len(full) <= MessageBuilder.discord_message_character_limit:
                return full
            else:
                formatting_length = len(self.mark + self.delimiter.join(self._before + self._after) + self.delimiter)
                main_message = self.delimiter.join(deque([self.title] if self.title is not None else []) + self._main)

                sub_messages = MessageBuilder.split_message(main_message, MessageBuilder.discord_message_character_limit - formatting_length)

                return [self.mark + self.delimiter.join(self._before + deque([sub_message]) + self._after) for sub_message in sub_messages]

    async def send(self):
        if self:
            full = self.get()
            if type(full) is not list:
                full = [full]

            for sub_message in full:
                for recipient in self.recipients:
                    discord_message = await recipient.send(sub_message)
                    
                    for callback in self._callbacks:
                        callback(discord_message)

    @staticmethod
    def split_message(message_string, character_limit, preferred_delimiters=["\n", ". ", " "]):
        result = []

        working = [message_string]

        # Split by preferred delimiters first, in order
        for delimiter in preferred_delimiters:
            working_split = []
            for sub_message in working:
                if len(sub_message) <= character_limit:
                    working_split.append(sub_message)
                else:
                    split_messages = sub_message.split(delimiter)
                    for split_message in split_messages[:-1]:
                        working_split.append(split_message + delimiter)
                    working_split.append(split_messages[-1])
            working = working_split

        # If messages are still too long, split down further without using delimiters
        working_split = []
        for sub_message in working:
            while sub_message:
                working_split.append(sub_message[:character_limit])
                sub_message = sub_message[character_limit:]
        working = working_split

        # Merge smaller messages where possible
        while working:
            working_message = ""

            while working and len((working_message + working[0]).strip("\n ")) <= character_limit:
                working_message += working[0]
                working = working[1:]

            result.append(working_message.strip("\n "))

        return result