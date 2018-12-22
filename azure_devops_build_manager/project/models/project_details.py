from msrest.serialization import Model

class ProjectDetails(Model):
    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'url': {'key': 'url', 'type': 'str'},
        'state': {'key': 'state', 'type': 'str'},
        'revision': {'key': 'revision', 'type': 'str'},
        'visibility': {'key': 'visibility', 'type': 'str'},
    }

    def __init__(self, id=None, name=None, url=None, state=None, revision=None, visibility=None):
        self.id = id
        self.name = name
        self.url = url
        self.state = state
        self.revision = revision
        self.visibility = visibility