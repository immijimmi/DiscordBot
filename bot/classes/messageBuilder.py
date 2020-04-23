from collections import deque

from .constants import Defaults

class MessageBuilder:
    def __init__(self, recipients=[], delimiter=Defaults.message_delimiter):
        self._delimiter = delimiter

        self._before = deque()
        self._main = deque()
        self._after = deque()

        self.recipients = list(recipients)
        self.title = ""
        self.mark = Defaults.message_mark

    def __bool__(self):
        return bool(self._main)  # If main is empty the message should be considered empty

    def add(self, item, to_bottom=True):
        if to_bottom:
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

    def get(self):
        if self:
            return self.mark + self._delimiter.join(self._before + deque([self.title]) + self._main + self._after)

    async def send(self):
        if self:
            for recipient in self.recipients:
                await recipient.send(self.get())
