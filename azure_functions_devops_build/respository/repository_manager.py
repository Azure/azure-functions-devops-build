# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
# Backward Compatible with Python 2.7
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'w')
from subprocess import STDOUT, check_call, check_output, CalledProcessError
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import vsts.git.v4_1.models.git_repository_create_options as git_repository_create_options

from ..base.base_manager import BaseManager
from . import models
from .local_git_utils import (
        git_init,
        git_add_remote,
        git_stage_all,
        git_commit,
        does_git_exist,
        does_git_remote_exist,
        construct_git_remote_name,
        construct_git_remote_url
)

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

    def check_if_git_exist(self) -> bool:
        return does_git_exist()

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

    def get_local_git_remote_name(self, repository_name, remote_prefix):
        return construct_git_remote_name(self._organization_name, self._project_name, repository_name, remote_prefix)

    # Since the portal url and remote url are same. We only need one function to handle portal access and git push
    def get_azure_devops_repo_url(self, repository_name):
        return construct_git_remote_url(self._organization_name, self._project_name, repository_name)

    # Check if the git repository exists first. If it does, check if the git remote exists.
    def check_if_local_git_remote_exists(self, repository_name, remote_prefix):
        if not self._repository_exists():
            return False

        remote_name = construct_git_remote_name(self._organization_name, self._project_name, repository_name, remote_prefix)
        return does_git_remote_exist(remote_name)

    # The function will initialize a git repo, create git remote, stage all changes, commit and push to remote
    # Exceptions: GitOperationException
    def setup_local_git_repository(self, repository_name, remote_prefix):
        """This command sets up a remote. It is normally used if a user already has a repository locally that they don't wish to get rid of"""

        remote_name = construct_git_remote_name(self._organization_name, self._project_name, repository_name, remote_prefix)
        remote_url = construct_git_remote_url(self._organization_name, self._project_name, repository_name)

        if self._repository_exists():
            git_init()

        git_add_remote(remote_name, remote_url)
        git_stage_all()
        git_commit("Create function app with azure devops build. Remote repository url: {url}".format(url=remote_url))
        git_push(remote_name)

    def _repository_exists(self):
        """Helper to see if gitfile exists"""
        return bool(os.path.exists('.git'))

    def list_github_repositories(self):
        """List github repositories if there are any from the current connection"""
        project = self._get_project_by_name(self._project_name)
        service_endpoints = self._service_endpoint_client.get_service_endpoints(project.id)
        github_endpoint = next((endpoint for endpoint in service_endpoints if endpoint.type == "github"), None)
        if github_endpoint is None:
            return []
        else:
            return self._build_client.list_repositories(project.id, 'github', github_endpoint.id)
