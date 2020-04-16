from objectExtensions import Extendable
from managedState import State
from managedState.registrar import Registrar

import json

from .responseBuilder import ResponseBuilder

class Handler(Extendable):
    DATA_FILENAME = "data.json"

    def __init__(self, client, extensions=[]):
        super().__init__(extensions)
        
        self.client = client
        
        self.state = State(extensions=[Registrar])
        self.LoadState()

        self.RegisterPaths()

    def RegisterPaths(self):
        pass

    def LoadState(self):
        try:
            with open(Handler.DATA_FILENAME, "r") as dataFile:
                self.state.set(json.loads(dataFile.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            pass

    def SaveState(self):
        with open(Handler.DATA_FILENAME, 'w') as dataFile:
            dataFile.write(json.dumps(self.state.Get()))

    def OnReady(self):
        pass

    def ProcessMessage(self, message):
        response = ResponseBuilder(recipients=[message.author])
        
        return response

    def StatusChange(self, before, after):
        response = ResponseBuilder()
        
        return response

    def UserOnline(self, before, after):
        response = ResponseBuilder(recipients=[after])
        
        return response
