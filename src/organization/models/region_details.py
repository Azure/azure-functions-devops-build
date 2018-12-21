from msrest.serialization import Model

class RegionDetails(Model):
    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'regionCode': {'key': 'regionCode', 'type': 'str'},
    }

    def __init__(self, id=None, display_name=None, regionCode=None):
        self.id = id
        self.display_name = display_name
        self.regionCode = regionCode