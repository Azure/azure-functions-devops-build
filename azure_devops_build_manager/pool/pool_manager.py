from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from . import models
from vsts.vss_connection import VssConnection

class PoolManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', creds=None, organization_name="", project_name=""):
        self.organization_name = organization_name
        self._project_name = project_name
        base_url = base_url.format(organization_name)
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
        #create the deserializer for the models
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self.organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')

    def get_pools(self):
        project = self.get_project_by_name(self._project_name)

        # Construct URL
        url = "/" + project.id + "/_apis/distributedtask/queues?actionFilter=16"

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.get(url, headers=header_paramters)
        response = self._client.send(request)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Pools', response)

        return deserialized

    def close_connection(self):
        self._client.close()

    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None