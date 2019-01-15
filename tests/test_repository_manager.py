# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.respository.repository_manager import RepositoryManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME
from ._helpers import get_credentials

class TestRepositoryManager(unittest.TestCase):

    def test_list_commits(self):
        creds = get_credentials()
        repository_manager = RepositoryManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        commits = (repository_manager.list_commits(REPOSITORY_NAME))

    def test_list_repositories(self):
        creds = get_credentials()
        repository_manager = RepositoryManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        repositories = repository_manager.list_repositories()
        

    def test_github(self):
        creds = get_credentials()
        repository_manager = RepositoryManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        print(repository_manager._github())

    def test_get_github(self):
        creds = get_credentials()
        repository_manager = RepositoryManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        for repo in (repository_manager._get_github_repsotories().repositories):
            print(repo)

if __name__ == '__main__':
    unittest.main()