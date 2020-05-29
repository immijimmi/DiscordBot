from ..constants import MessageFormats

class Permissions:
    levels = {
        "none": 0,
        "admin": 1
    }
    tags = [  # Only for generic tags. Plugin-specific tags should be added to their own lists inside the plugin constructor
        tag__hidden:="hidden"
    ]

    def __init__(self, level, tags):
        self.level = level
        self.tags = list(tags)

    def __str__(self):
        level_string = list(filter(lambda key: Permissions.levels[key] == self.level, Permissions.levels.keys()))[0]

        return "level: {0}\ntags: [{1}]".format(level_string, ", ".join(MessageFormats.format__list_item.format(tag) for tag in self.tags))

    def __eq__(self, other):
        self_tags_sorted = sorted(self.tags)
        other_tags_sorted = sorted(other.tags)

        return (
            self.level == other.level and
            len(self_tags_sorted) == len(other_tags_sorted) and
            all([self_tags_sorted[i] == other_tags_sorted[i] for i in range(len(self_tags_sorted))])
            )
    
    def __ne__(self, other):
        return (not self.__eq__(other))

    @property
    def data(self):
        return {"level": self.level, "tags": list(self.tags)}

    def is_permitted(self, *required_permissions_options):
        """Each object in required_permissions_options should be a permissions object that is considered to have exactly the required permissions.
        This allows multiple different types of permissions to grant access to a particular action"""
        for required_permissions in required_permissions_options:
            if self.level >= required_permissions.level and all([other_tag in self.tags for other_tag in required_permissions.tags]):
                return True
