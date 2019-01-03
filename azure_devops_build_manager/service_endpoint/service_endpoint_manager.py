
import vsts.service_endpoint.v4_1.models as models
from vsts.vss_connection import VssConnection
import uuid
import datetime
from msrest.serialization import TZ_UTC
from dateutil.relativedelta import relativedelta
import subprocess, json, requests

class ServiceEndpointManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", project_name="", creds=None):
        self._organization_name = organization_name
        self._project_name = project_name
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self._organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._agent_client = connection.get_client("vsts.task_agent.v4_1.task_agent_client.TaskAgentClient")
        self._build_client = connection.get_client('vsts.build.v4_1.build_client.BuildClient')
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._service_endpoint_client = connection.get_client('vsts.service_endpoint.v4_1.service_endpoint_client.ServiceEndpointClient')

    def create_service_endpoint(self, servicePrincipalName):
        project = self.get_project_by_name(self._project_name)
        
        print("Warning: we are using your current subscription as per the command 'az account show'. If you would like to use another subscription please change and use \
            'az account set'")

        command = "az account show --o json"
        token_resp = subprocess.check_output(command, shell=True).decode()
        account = json.loads(token_resp)

        data = {}
        data["subscriptionId"] = account['id']
        data["subscriptionName"] = account['name']
        data["environment"] = "AzureCloud"
        data["scopeLevel"] =  "Subscription"

        #need to generate a service principal here

        command = "az ad sp create-for-rbac --o json --name " + servicePrincipalName
        token_resp = subprocess.check_output(command, shell=True).decode()
        token_resp_dict = json.loads(token_resp)

        auth = models.endpoint_authorization.EndpointAuthorization(
            parameters= {
                "tenantid": token_resp_dict['tenant'],
                "serviceprincipalid": token_resp_dict['appId'],
                "authenticationType": "spnKey",
                "serviceprincipalkey": token_resp_dict['password']
            },
            scheme = "ServicePrincipal"
        )

        service_endpoint = models.service_endpoint.ServiceEndpoint(
            administrators_group=None,
            authorization=auth,
            data=data,
            name=token_resp_dict['displayName'],
            type="azurerm"        
        )

        self.endpoint = self._service_endpoint_client.create_service_endpoint(service_endpoint, project.id)

    def list_service_endpoints(self):
        project = self.get_project_by_name(self._project_name)
        return self._service_endpoint_client.get_service_endpoints(project.id)

    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None