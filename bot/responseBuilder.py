from collections import deque

class ResponseBuilder:
    def __init__(self, recipients=[], delimiter="\n"):
        self._delimiter = delimiter
        
        self._before = deque()
        self._main = deque()
        self._after = deque()

        self.recipients = list(recipients)

    def __bool__(self):
        return bool(self._main)  # If main is empty the response should be empty

    def Add(item, toFloor=True):
        if toFloor:
            self._main.append(item)

        else:
            self._main.appendleft(item)

    def Surround(item, inner=True, mirrored=True):
        if inner:
            self._before.append(item)
            self._after.appendleft(item[::-1] if mirrored else item)

        else:
            self._before.appendleft(item)
            self._after.append(item[::-1] if mirrored else item)

    def Get(self):
        if self:
            return self._delimiter.join(self._before + self._main + self._after)

    def Send(self):
        for recipient in self.recipients:
            recipient.send(self.Get())
