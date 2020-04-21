from managedState.registrar import KeyQueryFactory

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    timeout_duration = 5
