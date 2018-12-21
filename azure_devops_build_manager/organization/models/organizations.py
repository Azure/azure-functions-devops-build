from msrest.serialization import Model

class Organizations(Model):
    _attribute_map = {
        'count': {'key': 'count', 'type': 'int'},
        'value': {'key': 'value', 'type': '[OrganizationDetails]'},
    }

    def __init__(self, count=None, value=None):
        self.count = count
        self.value = value