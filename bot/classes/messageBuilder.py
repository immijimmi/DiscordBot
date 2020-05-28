from collections import deque

from .defaults import Defaults

class MessageBuilder:
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
        if self:
            return self.mark + self.delimiter.join(self._before + deque([self.title] if self.title is not None else []) + self._main + self._after)

    async def send(self):
        if self:
            for recipient in self.recipients:
                discord_message = await recipient.send(self.get())
                
                for callback in self._callbacks:
                    callback(discord_message)
