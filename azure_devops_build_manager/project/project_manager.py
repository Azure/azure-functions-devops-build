from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
from msrest.authentication import BasicAuthentication
from vsts.vss_connection import VssConnection
import vsts.core.v4_1.models.team_project as team_project
import vsts.core.v4_1.models.reference_links as reference_links
import re
import time
from . import models

class ProjectManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", creds=None, token=None, create_project_url='https://dev.azure.com'):
        self.organization_name = organization_name
        base_url = base_url.format(organization_name)
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
        self._credentials = creds
        #need to make a secondary client for the creating project as it uses a different base url
        self._create_project_config = Configuration(base_url= create_project_url)
        self._create_project_client = ServiceClient(creds, self._create_project_config)
        #create the deserializer for the models
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self.organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=self._credentials)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')

    def create_project(self, projectName):
        try:
            # set up the capabilities argument for creating a new project
            capabilities = dict()
            capabilities['versioncontrol'] =  {"sourceControlType": "Git"}
            capabilities['processTemplate'] = {"templateTypeId": "adcc42ab-9882-485e-a3ed-7678f01f66bc"}
            t_proj = team_project.TeamProject(description="", name=projectName, visibility=0, capabilities=capabilities)
            res = self._core_client.queue_create_project(t_proj)
            id = res.id
            # Poll project until it has finished
            self.poll_project(id)
            # Find the new project we have created
            project = self.get_project_by_name(projectName)
            return project
        except Exception as e:
            print(e)
            return e

    #get existing projects
    def get_existing_projects(self):
        #construct url
        url = '/_apis/projects'

        #construct query parameters
        query_paramters = {}
        query_paramters['includeCapabilities'] = 'true'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'
        
        request = self._client.get(url, params=query_paramters)
        response = self._client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Projects', response)

        return deserialized


    def poll_project(self, id):
        project_created = False
        while (not project_created):
            time.sleep(1)
            #check if it has been created
            res = self.is_project_created(id)
            print('status is: ', res.status)
            try:
                if res.status == 'succeeded':
                    project_created = True
            except:
                break


    def is_project_created(self, id):
        #construct url
        url = '/' + self.organization_name + '/_apis/operations/' + id

        #construct query parameters
        query_paramters = {}

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'
        
        request = self._create_project_client.get(url, params=query_paramters)
        response = self._create_project_client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('ProjectPoll', response)

        return deserialized

    def get_project_by_name(self, name):
        time.sleep(0.3)
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None