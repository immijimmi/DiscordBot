from objectExtensions import Extendable
from managedState import State, KeyQuery
from managedState.registrar import Registrar, KeyQueryFactory
from managedState.listeners import Listeners

import json

from .constants import KeyQueryFactories
from .classes.responseBuilder import ResponseBuilder
from .classes.eventTimeout import EventTimeout

class Handler(Extendable):
    data_filename = "data.json"

    def __init__(self, client, extensions=[]):
        self.client = client

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self.state.add_listener("set", lambda metadata: self._save_state())
        self._register_paths()

        self.timeouts = {}
        self.responses_working = []

        super().__init__(extensions)

    def get_member(self, member_identifier, requester=None):
        if requester and type(member_identifier) == str:
            user_nicknames = self.state.registered_get("user_nicknames", [requester.id])

            for member_id in user_nicknames:
                if user_nicknames[member_id].lower() == member_identifier.lower():
                    member_identifier = member_id
                    break
        
        for member in self.client.get_all_members():
            if member.id == member_identifier:
                return member

            elif type(member_identifier) == str and "#" in member_identifier:
                if "{0}#{1}".format(member.name, member.discriminator).lower() == member_identifier.lower():
                    return member

    def get_member_name(self, member, requester=None):
        if requester:
            user_nicknames = self.state.registered_get("user_nicknames", [requester.id])

            if member.id in user_nicknames:
                return user_nicknames[member.id]

        return "{0}#{1}".format(member.name, member.discriminator)

    async def send_responses(self):
        while self.responses_working:
            response = self.responses_working.pop(0)

            if response:
                await response.send()

    # Event function
    def on_ready(self):
        pass

    # Event function
    def process_message(self, message):
        timeout_key = "process_message|{0}|{1}".format(message.author.id, message.content)
        timeout = self.timeouts.get(timeout_key, None)

        if not timeout or timeout.is_expired():
            self.timeouts[timeout_key] = EventTimeout(timeout_key)
            
            response = ResponseBuilder(recipients=[message.author])
            
            self.responses_working.append(response)

    # Event function
    def user_online(self, before, after):
        timeout_key = "user_online|{0}".format(after.id)
        timeout = self.timeouts.get(timeout_key, None)
        
        if not timeout or timeout.is_expired():
            self.timeouts[timeout_key] = EventTimeout(timeout_key)
            
            response = ResponseBuilder(recipients=[after])

            self.responses_working.append(response)
    
    def _load_state(self):
        try:
            with open(Handler.data_filename, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            pass

    def _save_state(self):
        with open(Handler.data_filename, 'w') as data_file:
            data_file.write(json.dumps(self.state.get()))

    def _register_paths(self):
        self.state.register("all_users_settings", ["user_settings"], [{}])
        self.state.register("user_nicknames", ["user_settings", KeyQueryFactories.user_id, "nicknames"], [{}, {}, {}])
