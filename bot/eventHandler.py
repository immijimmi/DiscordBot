from managedState import State, KeyQuery
from managedState.registrar import Registrar, KeyQueryFactory
from managedState.listeners import Listeners

import json
import logging
from collections import deque

from .constants import KeyQueryFactories, Defaults, Methods, MessageFormats
from .plugins.essentials import Essentials
from .plugins.meta import Meta
from .classes.permissions import Permissions
from .classes.messageBuilder import MessageBuilder
from .classes.eventTimeout import EventTimeout
from .classes.timeoutDuration import TimeoutDuration

class EventHandler():
    def __init__(self, client, plugins=[]):
        self._timeouts = {}  # Stores cooldowns for specific bot actions
        self._callbacks = deque()  # Stores async callbacks created by plugins

        self.client = client

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()

        self.state.add_listener("set", lambda metadata: self._save_state())
        self._register_paths()

        self.plugins = (Essentials(self), Meta(self)) + tuple(plugin(self) for plugin in plugins)

    def add_callback(self, callback, to_end=False):  # Callbacks added with to_end as True will be called last
        if to_end:
            self._callbacks.appendleft(callback)  # Callbacks are popped and ran so index 0 is the last
        else:
            self._callbacks.append(callback)

    def try_trigger_timeout(self, timeout_key, new_timeout_duration):
        timeout = self._timeouts.get(timeout_key, None)

        is_active_timeout = timeout and not timeout.is_expired()
        if is_active_timeout:
            return False
        else:
            self._timeouts[timeout_key] = EventTimeout(timeout_key, new_timeout_duration)
            return True

    def try_delete_timeout(self, timeout_key):
        if timeout_key in self._timeouts:
            del self._timeouts[timeout_key]
            return True

    #Event method
    async def on_ready(self):
        responses = []

        for plugin in self.plugins:
            plugin_responses = plugin.on_ready()

            responses += plugin_responses if plugin_responses else []

        await self._send_responses(responses)
        await self._run_callbacks()

    #Event method
    async def process_private_message(self, message):
        timeout_triggered = self.try_trigger_timeout("process_private_message|{0}|{1}".format(message.author.id, message.content), Defaults.timeout_duration)

        if timeout_triggered:
            response = MessageBuilder(recipients=[message.author])
        else:
            response = None
            
        responses = [response]

        for plugin in self.plugins:
            plugin_responses = plugin.process_private_message(message, handler_response=response)

            responses += plugin_responses if plugin_responses else []

        # If none of the plugins could process the message and return a response
        if not responses[0] and type(responses[0]) is MessageBuilder:
            responses[0].add("Unrecognised command: " + MessageFormats.format__user_input.format(message.content))

        await self._send_responses(responses)
        await self._run_callbacks()

    # Event method
    async def process_public_message(self, message):
        timeout_triggered = self.try_trigger_timeout("process_public_message|{0}|{1}".format(message.author.id, message.content), Defaults.timeout_duration)

        if timeout_triggered:
            response = MessageBuilder(recipients=[message.channel])
        else:
            response = None

        responses = [response]

        for plugin in self.plugins:
            plugin_responses = plugin.process_public_message(message, handler_response=response)

            responses += plugin_responses if plugin_responses else []

        # If none of the plugins could process the message and return a response
        if not responses[0] and type(responses[0]) is MessageBuilder:
            pass

        await self._send_responses(responses)
        await self._run_callbacks()

    #Event method
    async def user_online(self, before, after):
        setting_enabled = self.state.registered_get("user_welcome_enabled", [str(after.id)])

        response = None
        if setting_enabled:
            new_timeout_duration = TimeoutDuration(self.state.registered_get("user_welcome_timeout_seconds", [str(after.id)]))
            timeout_triggered = self.try_trigger_timeout("user_welcome|{0}".format(after.id), new_timeout_duration)
            
            if timeout_triggered:
                response = MessageBuilder(recipients=[after])
                response.title = "**Welcome back!**"

        responses = [response]

        for plugin in self.plugins:
            plugin_responses = plugin.user_online(before, after, handler_response=response)

            responses += plugin_responses if plugin_responses else []

        await self._send_responses(responses)
        await self._run_callbacks()

    #Event method
    async def user_away(self, before, after):
        responses = []

        for plugin in self.plugins:
            plugin_responses = plugin.user_away(before, after)

            responses += plugin_responses if plugin_responses else []

        await self._send_responses(responses)
        await self._run_callbacks()

    def try_get_member(self, member_identifier, requester_id=None):
        member_identifier = Methods.clean(str(member_identifier))  # Coalesce types to string only
        nickname_id_string = str(self.try_get_id(member_identifier, requester_id))
        
        member_list = list(self.client.get_all_members())

        if nickname_id_string:
            for member in member_list:
                if str(member.id) == nickname_id_string:
                    return member

        for member in member_list:
            if str(member.id) == member_identifier:
                return member

            if "#" in member_identifier:
                if Methods.clean("{0}#{1}".format(member.name, member.discriminator)).lower() == member_identifier.lower():
                    return member

    def try_get_id(self, nickname, requester_id):
        nickname = Methods.clean(nickname)

        user_nicknames = self.state.registered_get("user_nicknames", [str(requester_id)])

        for nickname_id_string in user_nicknames:
            if Methods.clean(user_nicknames[nickname_id_string]).lower() == nickname.lower():
                return int(nickname_id_string)

    def try_get_nickname(self, user_id, requester_id):
        user_id = Methods.clean(str(user_id))

        user_nicknames = self.state.registered_get("user_nicknames", [str(requester_id)])

        for nickname_id_string in user_nicknames:
            if nickname_id_string == user_id:
                return user_nicknames[nickname_id_string]

    def get_member_name(self, member, requester_id=None):
        if requester_id:
            user_nicknames = self.state.registered_get("user_nicknames", [str(requester_id)])

            if str(member.id) in user_nicknames:
                return Methods.clean(user_nicknames[str(member.id)])

        return Methods.clean("{0}#{1}".format(member.name, member.discriminator))

    async def _run_callbacks(self):
        while self._callbacks:
            await self._callbacks.pop()()

    async def _send_responses(self, responses):
        while responses:
            response = responses.pop(0)

            if response:
                await response.send()

    def _load_state(self):
        try:
            with open(Defaults.state_filename, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Defaults.state_filename, 'w') as data_file:
            data_file.write(json.dumps(self.state.get()))

    def _register_paths(self):
        self.state.register("all_users_settings", ["user_settings"], [{}])
        self.state.register("user_nicknames", ["user_settings", KeyQueryFactories.dynamic_key, "nicknames"], [{}, {}, {}])
        self.state.register("user_welcome_timeout_seconds", ["user_settings", KeyQueryFactories.dynamic_key, "welcome", "timeout_duration"], [{}, {}, {}, Defaults.timeout_duration.seconds])
        self.state.register("user_welcome_enabled", ["user_settings", KeyQueryFactories.dynamic_key, "welcome", "enabled"], [{}, {}, {}, True])
        self.state.register("user_permissions_data", ["user_settings", KeyQueryFactories.dynamic_key, "permissions"], [{}, {}, Defaults.permissions.data])
