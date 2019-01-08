# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from subprocess import DEVNULL, STDOUT, check_call
import os

import vsts.git.v4_1.models.git_repository_create_options as git_repository_create_options

from azure_devops_build_manager.base.base_manager import BaseManager
from . import models


class RepositoryManager(BaseManager):
    """ Manage DevOps repositories

    Attributes:
        See BaseManager
    """

    def __init__(self, organization_name="", project_name="", creds=None):
        super(RepositoryManager, self).__init__(creds, organization_name=organization_name, project_name=project_name)

    def create_repository(self, repository_name):
        """Create a new azure functions git repository"""
        project = self._get_project_by_name(self._project_name)
        git_repo_options = git_repository_create_options.GitRepositoryCreateOptions(name=repository_name, project=project)
        return self._git_client.create_repository(git_repo_options)

    def list_repositories(self):
        """List the current repositories in a project"""
        return self._git_client.get_repositories(self._project_name)

    def setup_repository(self, repository_name):
        """This command sets up the repository locally - it initialises the git file and creates the initial push ect"""
        if self._repository_exists():
            message = """There is already an existing repository in this folder. If it is a github repository please
                         create an access token and then use the command 'az functionapp devops-build repository github
                         --token {OATH TOKEN}' If this is not an exisitng github or azure devops repository we are unable
                          to support a build through azure devops. Please either delete the reference to the repository in the current folder. 
                      """
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
        return True if os.path.exists('.git') else False

    def _github(self):
        """
        TODO: setup the github integration to be able to do builds that are triggered by github!
        """
