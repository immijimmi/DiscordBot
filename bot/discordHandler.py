from managedState import State, KeyQuery
from managedState.registrar import Registrar, KeyQueryFactory
from managedState.listeners import Listeners

import json
import logging

from .constants import KeyQueryFactories, Defaults, MessageFormats
from .classes.messageBuilder import MessageBuilder
from .classes.eventTimeout import EventTimeout

class Handler():
    data_filename = "data.json"

    def __init__(self, client, plugins=[]):
        self.timeouts = {}

        self.client = client

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self.state.add_listener("set", lambda metadata: self._save_state())
        self._register_paths()

        self.plugins = [plugin(self) for plugin in plugins]

    #Event method
    async def on_ready(self):
        responses = []

        for plugin in self.plugins:
            plugin_responses = plugin.on_ready()

            responses += plugin_responses if plugin_responses else []

        await Handler.send_responses(responses)

    #Event method
    async def process_message(self, message):
        timeout_triggered = self.try_trigger_timeout("process_message|{0}|{1}".format(message.author.id, message.content), Defaults.timeout_duration)

        if timeout_triggered:
            response = MessageBuilder(recipients=[message.author])
        else:
            response = None
            
        responses = [response]

        for plugin in self.plugins:
            plugin_responses = plugin.process_message(message, handler_response=response)

            responses += plugin_responses if plugin_responses else []

        # If none of the plugins could process the message and return a response
        if not responses[0] and type(responses[0]) is MessageBuilder:
            responses[0].add("Unrecognised command: `{0}`".format(message.content) + "\n")

        await Handler.send_responses(responses)

    #Event method
    async def user_online(self, before, after):
        setting_enabled = self.state.registered_get("user_welcome_enabled", [str(after.id)])

        response = None
        if setting_enabled:
            new_timeout_duration = self.state.registered_get("user_welcome_timeout_duration", [str(after.id)])
            timeout_triggered = self.try_trigger_timeout("user_welcome|{0}".format(after.id), new_timeout_duration)
            
            if timeout_triggered:
                response = MessageBuilder(recipients=[after])
                response.title = MessageFormats.welcome_header + "\n"

        responses = [response]

        for plugin in self.plugins:
            plugin_responses = plugin.user_online(before, after, handler_response=response)

            responses += plugin_responses if plugin_responses else []

        await Handler.send_responses(responses)

    def get_member(self, member_identifier, requester=None):
        member_identifier = str(member_identifier)  # Coalesce types to string only
        
        if requester:
            user_nicknames = self.state.registered_get("user_nicknames", [str(requester.id)])

            for nickname_id_string in user_nicknames:
                if user_nicknames[nickname_id_string].lower() == member_identifier.lower():
                    member_identifier = nickname_id_string
                    break
        
        for member in self.client.get_all_members():  # Returns None if the member cannot be found
            if str(member.id) == member_identifier:
                return member

            elif "#" in member_identifier:
                if "{0}#{1}".format(member.name, member.discriminator).lower() == member_identifier.lower():
                    return member

    def get_member_name(self, member, requester=None):
        if requester:
            user_nicknames = self.state.registered_get("user_nicknames", [str(requester.id)])

            if str(member.id) in user_nicknames:
                return user_nicknames[str(member.id)]

        return "{0}#{1}".format(member.name, member.discriminator)

    def try_trigger_timeout(self, timeout_key, new_timeout_duration):
        timeout = self.timeouts.get(timeout_key, None)

        is_active_timeout = timeout and not timeout.is_expired()

        if not is_active_timeout:
            if timeout:
                timeout.reset()
            else:
                self.timeouts[timeout_key] = EventTimeout(timeout_key, duration_seconds=new_timeout_duration)

            return True

        return False

    @staticmethod
    async def send_responses(responses):
        while responses:
            response = responses.pop(0)

            if response:
                await response.send()
    
    def _load_state(self):
        try:
            with open(Handler.data_filename, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Handler.data_filename, 'w') as data_file:
            data_file.write(json.dumps(self.state.get()))

    def _register_paths(self):
        self.state.register("all_users_settings", ["user_settings"], [{}])
        self.state.register("user_nicknames", ["user_settings", KeyQueryFactories.dynamic_key, "nicknames"], [{}, {}, {}])
        self.state.register("user_welcome_timeout_duration", ["user_settings", KeyQueryFactories.dynamic_key, "welcome", "timeout_duration"], [{}, {}, {}, Defaults.timeout_duration])
        self.state.register("user_welcome_enabled", ["user_settings", KeyQueryFactories.dynamic_key, "welcome", "enabled"], [{}, {}, {}, True])
