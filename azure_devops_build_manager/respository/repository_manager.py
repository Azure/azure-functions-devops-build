from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
from msrest.authentication import BasicAuthentication
from vsts.vss_connection import VssConnection
import vsts.core.v4_1.models.team_project as team_project
import vsts.core.v4_1.models.reference_links as reference_links
import vsts.git.v4_1.models.git_repository_create_options as git_repository_create_options
import re
import time
import os

class RepositoryManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", project_name="", creds=None, create_project_url='https://dev.azure.com'):
        self.organization_name = organization_name
        self.project_name = project_name
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self.organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._git_client = connection.get_client("vsts.git.v4_1.git_client.GitClient")

    def repository_exists(self):
        if os.path.exists('.git'):
            return True
        else:
            return False

    """
    This command creates a new azure functions git repository
    """
    def create_repository(self, repository_name):
        project = self.get_project_by_name(self.project_name)
        git_repo_options = git_repository_create_options.GitRepositoryCreateOptions(name=repository_name, project=project)
        try:
            repository = self._git_client.create_repository(git_repo_options)
            return repository
        except Exception as e:
            return e


    def list_repositories(self):
        repositories = self._git_client.get_repositories(self.project_name)
        return repositories

    """
    This command sets up the repository locally - it initialises the git file and creates the initial push ect.
    """
    def setup_repository(self, repository_name):
        if self.repository_exists():
            error = {}
            error['message'] = """There is already an existing repository in this folder. If it is a github repository please create an
                                  access token and then use the command 'az functionapp devops-build repository github --token {OATH TOKEN}'
                                  If this is not an exisitng github or azure devops repository we are unable to support a build through azure
                                  devops. Please either delete the reference to the repository in the current folder. """
            return error
        else:
            origin_command = "git remote add origin https://" + self.organization_name + ".visualstudio.com/" + self.project_name + "/_git/" + repository_name
            os.system("git init")
            os.system("git add -A")
            os.system("git commit -a -m \"creating functions app\"")
            os.system(origin_command)
            os.system("git push -u origin --all")

    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None


    def github(self):
        """
        TODO: setup the github integration to be able to do builds that are triggered by github!
        """