# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import vsts.build.v4_1.models as build_models

from azure_devops_build_manager.base.base_manager import BaseManager
from azure_devops_build_manager.pool.pool_manager import PoolManager


class BuilderManager(BaseManager):
    """ Manage DevOps Builds

    Attributes:
        build_client : client to access build devops features (build definitions, builds, build artifacts ect.)
        core_client : client to access core devops features (projects, organizations ect.)
    """

    def __init__(self, organization_name="", project_name="", repository_name="", creds=None):
        """Inits BuilderManager as per BaseManager and includes relevant clients"""
        super(BuilderManager, self).__init__(organization_name, project_name, creds, repository_name=repository_name)
        self._agent_client = self._connection.get_client("vsts.task_agent.v4_1.task_agent_client.TaskAgentClient")
        self._build_client = self._connection.get_client('vsts.build.v4_1.build_client.BuildClient')
        self._core_client = self._connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._git_client = self._connection.get_client("vsts.git.v4_1.git_client.GitClient")

    def create_definition(self, build_definition_name, pool_name):
        # get the project and repository objects
        project = self.get_project_by_name(self._project_name)
        repository = self.get_repository_by_name(project, self._repository_name)
        pool = self.get_pool_by_name(pool_name)
        pool_queue = build_models.agent_pool_queue.AgentPoolQueue(id=pool.id, name=pool_name)
        # find the references to the repository and projects
        build_repository = build_models.build_repository.BuildRepository(default_branch="master", id=repository.id, name=repository.name, type="TfsGit")
        team_project_reference = self.get_project_reference(project)

        # create the definition of the build definition
        build_definition_definition = self.get_build_definition(team_project_reference, build_repository, build_definition_name, pool_queue)

        # create the definition itself
        build_definition = self._build_client.create_definition(build_definition_definition, project=project.name)

        return build_definition

    def list_definitions(self):
        project = self.get_project_by_name(self._project_name)
        return self._build_client.get_definitions(project=project.id)

    def create_build(self, build_definition_name, pool_name):
        pool = self.get_pool_by_name(pool_name)
        # get the project object
        project = self.get_project_by_name(self._project_name)
        definition = self.get_definition_by_name(project, build_definition_name)
        # find the references to the project and to the build definition
        team_project_reference = self.get_project_reference(project)
        build_definition_reference = self.get_build_definition_reference(team_project_reference, definition)

        pool_queue = build_models.agent_pool_queue.AgentPoolQueue(id=pool.id, name=pool_name)
        build = build_models.build.Build(definition=build_definition_reference, queue=pool_queue)
        return self._build_client.queue_build(build, project=project.id)

    def list_builds(self):
        project = self.get_project_by_name(self._project_name)
        return self._build_client.get_builds(project=project.id)

    def get_pool_by_name(self, pool_name):
        pool_manager = PoolManager(organization_name=self._organization_name, project_name=self._project_name, creds=self._creds)
        pools = pool_manager.get_pools()
        for pool in pools.value:
            if pool.name == pool_name:
                return pool
        return None

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

    def get_build_definition(self, team_project_reference, build_repository, build_definition_name,pool_queue):
        process = self.get_process()
        build_def = build_models.build_definition.BuildDefinition(
            project=team_project_reference,
            type=2,
            name=build_definition_name,
            process=process,
            repository=build_repository,
            queue=pool_queue
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