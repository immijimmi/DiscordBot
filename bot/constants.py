from managedState.registrar import KeyQueryFactory

class KeyQueryFactories:
    user_id = KeyQueryFactory(lambda sub_state, user_id: user_id)
