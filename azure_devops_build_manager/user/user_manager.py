from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from . import models

class UserManager(object):

    def __init__(self, base_url='https://peprodscussu2.portalext.visualstudio.com', creds=None):
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
        #create the deserializer for the models
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        
    def get_user_id(self):
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        request = self._client.get('/_apis/AzureTfs/UserContext')
        response = self._client.send(request, header_parameters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('User', response)

        return deserialized

    def close_connection(self):
        self._client.close()