from managedState import State
from managedState.registrar import Registrar

import json

class DiscordHandler:
    def __init__(self, client):
        self.client = client
        self.state = State(extensions=[Registrar])

        self.LoadState()

    def LoadState(self):
        try:
            with open(Data.filename, "r") as dataFile:
                self.state.set(json.loads(dataFile.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            pass

    def SaveState(self):
        with open(Data.filename, 'w') as dataFile:
            dataFile.write(json.dumps(self.state.Get()))
