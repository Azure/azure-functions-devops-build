from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from . import models

class ProjectManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", creds=None, create_project_url='https://dev.azure.com'):
        base_url = base_url.format(organization_name)
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
        #need to make a secondary client for the creating project as it uses a different base url
        self._create_project_config = Configuration(base_url= create_project_url)
        self._create_organization_client = ServiceClient(creds, self._create_project_config)
        #create the deserializer for the models
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)


    def create_project(self):
        #get a valid name
        created = False
        while(created == False):
            projectName = input("enter the name of the project you wish to make:")
            try:
                organization_url = 'https://dev.azure.com/' + self.organization.name
                # Create a connection to the org
                connection = VssConnection(base_url=organization_url, creds=self.user.credentials)
                # Get a client (the "core" client provides access to projects, teams, etc)
                core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
                capabilities = dict()
                capabilities['versioncontrol'] =  {"sourceControlType": "Git"}
                capabilities['processTemplate'] = {"templateTypeId": "adcc42ab-9882-485e-a3ed-7678f01f66bc"}
                t_proj = team_project.TeamProject(description="", name=projectName, visibility=0, capabilities=capabilities)
                res = core_client.queue_create_project(t_proj)
                self.id = res.id
                self.name = projectName
            except Exception as e:
                print(e)
                continue
            created = True
        self.poll_project()

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


    def poll_project(self):
        project_created = False
        while (not project_created):
            time.sleep(1)
            #check if it has been created
            res = self.is_project_created()
            print('status is: ', res['status'])
            try:
                if res['status'] == 'succeeded':
                    project_created = True
            except:
                break

        #we now need to replace the queing id with the newly made project id!
        connection = VssConnection(base_url='https://dev.azure.com/' + self.organization.name, creds=self.user.credentials)
        client = connection.get_client('vsts.core.v4_1.core_client.CoreClient')

        for p in client.get_projects():
            if p.name == self.name:
                self.id = p.id

    def is_project_created(self):
        base_url = 'https://dev.azure.com/' + self.organization.name + '/_apis/operations/' + self.id
        headers = {
            'Accept' : 'application/json',
            'Authorization' : 'Bearer ' + self.user.bearerToken
            }
        req = requests.get(base_url, headers=headers)
        return req.json()
