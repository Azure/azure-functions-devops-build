import vsts.service_endpoint.v4_1.models as models
from vsts.vss_connection import VssConnection
import uuid

class ArtifactManager(object):

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

    def list_artifacts(self, build_id):
        project = self.get_project_by_name(self._project_name)
        return self._build_client.get_artifacts(build_id, project)

    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None