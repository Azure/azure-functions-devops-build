# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
import os

from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import vsts.git.v4_1.models.git_repository_create_options as git_repository_create_options

from ..base.base_manager import BaseManager
from . import models


class RepositoryManager(BaseManager):
    """ Manage DevOps repositories

    Attributes:
        See BaseManager
    """

    def __init__(self, organization_name="", project_name="", creds=None):
        base_url = 'https://dev.azure.com'
        self._config = Configuration(base_url=base_url)
        self._client = ServiceClient(creds, self._config)
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        super(RepositoryManager, self).__init__(creds, organization_name=organization_name, project_name=project_name)

    def create_repository(self, repository_name):
        """Create a new azure functions git repository"""
        project = self._get_project_by_name(self._project_name)
        git_repo_options = git_repository_create_options.GitRepositoryCreateOptions(name=repository_name, project=project)
        return self._git_client.create_repository(git_repo_options)

    def list_repositories(self):
        """List the current repositories in a project"""
        return self._git_client.get_repositories(self._project_name)

    def list_commits(self, repository_name):
        """List the commits for a given repository"""
        project = self._get_project_by_name(self._project_name)
        repository = self._get_repository_by_name(project, repository_name)
        return self._git_client.get_commits(repository.id, None, project=project.id)

    def setup_remote(self, repository_name, remote_name):
        """This command sets up a remote. It is normally used if a user already has a repository locally that they don't wish to get rid of"""
        if self._remote_exists(remote_name):
            message = """There is already an remote with this name."""
            succeeded = False
        else:
            origin_command = ["git", "remote", "add", remote_name, "https://" + self._organization_name + \
                                        ".visualstudio.com/" + self._project_name + "/_git/" + repository_name]
            check_call(origin_command, stdout=DEVNULL, stderr=STDOUT)
            check_call('git add -A'.split(), stdout=DEVNULL, stderr=STDOUT)
            try:
                check_call(["git", "commit", "-a", "-m", "\"creating functions app\""], stdout=DEVNULL, stderr=STDOUT)
            except CalledProcessError:
                print("no need to commit anything")
            check_call(('git push ' + remote_name + ' --all').split(), stdout=DEVNULL, stderr=STDOUT)
            message = "succeeded"
            succeeded = True
        return models.repository_response.RepositoryResponse(message, succeeded)

    def setup_repository(self, repository_name):
        """This command sets up the repository locally - it initialises the git file and creates the initial push ect"""
        if self._repository_exists():
            message = """There is already an existing repository in this folder."""
            succeeded = False
        else:
            origin_command = ["git", "remote", "add", "origin", "https://" + self._organization_name + \
                              ".visualstudio.com/" + self._project_name + "/_git/" + repository_name]
            check_call('git init'.split(), stdout=DEVNULL, stderr=STDOUT)
            check_call('git add -A'.split(), stdout=DEVNULL, stderr=STDOUT)
            check_call(["git", "commit", "-a", "-m", "\"creating functions app\""], stdout=DEVNULL, stderr=STDOUT)
            check_call(origin_command, stdout=DEVNULL, stderr=STDOUT)
            check_call('git push -u origin --all'.split(), stdout=DEVNULL, stderr=STDOUT)
            message = "succeeded"
            succeeded = True
        return models.repository_response.RepositoryResponse(message, succeeded)

    def _repository_exists(self):
        """Helper to see if gitfile exists"""
        return bool(os.path.exists('.git'))

    def _remote_exists(self, remote_name):
        lines = (check_output('git remote show'.split())).decode('utf-8').split('\n')
        for line in lines:
            if line == remote_name:
                return True
        return False

    def list_github_repositories(self):
        """List github repositories if there are any from the current connection"""
        project = self._get_project_by_name(self._project_name)
        service_endpoints = self._service_endpoint_client.get_service_endpoints(project.id)
        github_endpoint = next((endpoint for endpoint in service_endpoints if endpoint.type == "github"), None)
        if github_endpoint is None:
            return []
        else:
            return self._build_client.list_repositories(project.id, 'github', github_endpoint.id)
