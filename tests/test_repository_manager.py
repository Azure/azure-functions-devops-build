# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.repository.repository_manager import RepositoryManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, CREATE_DEVOPS_OBJECTS
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

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                    "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_initial_setup(self):
        creds = get_credentials()
        repository_manager = RepositoryManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        setup = repository_manager.setup_repository(REPOSITORY_NAME)

if __name__ == '__main__':
    unittest.main()
