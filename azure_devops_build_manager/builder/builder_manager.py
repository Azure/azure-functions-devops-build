from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication
import vsts.core.v4_1.models as core_models
import vsts.build.v4_1.models as build_models
import vsts.task_agent.v4_1.models as task_agent_models
import datetime
import os
import requests
import pick

class BuilderManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", project_name="", repository_name="", creds=None):
        self._organization_name = organization_name
        self._project_name = project_name
        self._repository_name = repository_name
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self._organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._agent_client = connection.get_client("vsts.task_agent.v4_1.task_agent_client.TaskAgentClient")
        self._build_client = connection.get_client('vsts.build.v4_1.build_client.BuildClient')
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._git_client = connection.get_client("vsts.git.v4_1.git_client.GitClient")

    def create_definition(self, build_definition_name):
        # get the project and repository objects
        project = self.get_project_by_name(self._project_name)
        repository = self.get_repository_by_name(project, self._repository_name)

        # find the references to the repository and projects
        build_repository = build_models.build_repository.BuildRepository(default_branch="master", id=repository.id, name=repository.name, type="TfsGit")
        team_project_reference = self.get_project_reference(project)

        # create the definition of the build definition
        build_definition_definition = self.get_build_definition(team_project_reference, build_repository, build_definition_name)

        # create the definition itself
        build_definition = self._build_client.create_definition(build_definition_definition, project=project.name)

        return build_definition

    def list_definitions(self):
        project = self.get_project_by_name(self._project_name)
        return self._build_client.get_definitions(project=project.id)

    def create_build(self, build_definition_name, poolId, poolName):
        # get the project object
        project = self.get_project_by_name(self._project_name)
        definition = self.get_definition_by_name(project, build_definition_name)
        # find the references to the project and to the build definition
        team_project_reference = self.get_project_reference(project)
        build_definition_reference = self.get_build_definition_reference(team_project_reference, definition)

        pool_queue = build_models.agent_pool_queue.AgentPoolQueue(id=poolId, name=poolName)
        build = build_models.build.Build(definition=build_definition_reference, queue=pool_queue)
        self.build = self._build_client.queue_build(build, project=project.id)


    def get_process(self):
        process = {}
        process["yamlFilename"] = "azure-pipelines.yml"
        process["type"] = 2
        process["resources"] = {}
        return process


    def get_project_reference(self, project):
        team_project_ref = build_models.team_project_reference.TeamProjectReference(
            abbreviation=project.abbreviation,
            description=project.description,
            id=project.id, 
            name=project.name,
            revision=project.revision,
            state=project.state,
            url=project.url,
            visibility=project.visibility
            )
        return team_project_ref

    def get_build_definition(self, team_project_reference, build_repository, build_definition_name):
        process = self.get_process()
        build_def = build_models.build_definition.BuildDefinition(
            project=team_project_reference,
            type=2,
            name=build_definition_name,
            process=process,
            repository=build_repository,
        )
        return build_def

    def get_build_definition_reference(self, team_project_reference, build_definition):
        build_definition_reference = build_models.definition_reference.DefinitionReference(
            created_date= build_definition.created_date,
            project=team_project_reference, 
            type=build_definition.type,
            name=build_definition.name,
            id=build_definition.id
        )
        return build_definition_reference


    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None

    def get_repository_by_name(self, project, name):
        for p in self._git_client.get_repositories(project.id):
            if p.name == name:
                return p
        return None

    def get_definition_by_name(self, project, name):
        for p in self._build_client.get_definitions(project.id):
            if p.name == name:
                return p
        return None