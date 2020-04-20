from objectExtensions import Extension

from ...discordHandler import Handler

class NicknameSettings(Extension):
    @staticmethod
    def extend(target_instance):
        pass

    @staticmethod
    def can_extend(target_instance):
        return type(target_instance) is Handler

    ##### TODO
