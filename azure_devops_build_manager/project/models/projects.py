from msrest.serialization import Model

class Projects(Model):
    _attribute_map = {
        'count': {'key': 'count', 'type': 'int'},
        'value': {'key': 'value', 'type': '[ProjectDetails]'},
    }

    def __init__(self, count=None, value=None):
        self.count = count
        self.value = value