from msrest.serialization import Model

class User(Model):
    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'displayName': {'key': 'displayName', 'type': 'str'},
        'uniqueName': {'key': 'uniqueName', 'type': 'str'},
        'email': {'key': 'email', 'type': 'str'},
        'preferredTimeZoneOffset': {'key': 'preferredTimeZoneOffset', 'type': 'str'},
    }

    def __init__(self, id=None, displayName=None, uniqueName=None, email=None, preferredTimeZoneOffset=None):
        self.id = id
        self.displayName = displayName
        self.uniqueName = uniqueName
        self.email = email
        self.preferredTimeZoneOffset = preferredTimeZoneOffset