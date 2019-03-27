# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.repository.repository_manager import RepositoryManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, CREATE_DEVOPS_OBJECTS
from ._helpers import get_credentials

class TestRepositoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.repository_manager = RepositoryManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )

    def test_get_repo_branches(self):
        result = self.repository_manager.get_azure_devops_repository_branches(REPOSITORY_NAME)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    def test_get_repo(self):
        result = self.repository_manager.get_azure_devops_repository(REPOSITORY_NAME)
        if result is not None:
            self.assertEqual(result.name, REPOSITORY_NAME)

    def test_invalid_get_repo_bad_name(self):
        result = self.repository_manager.get_azure_devops_repository("bad@name")
        self.assertIsNone(result)

    def test_create_repository(self):
        result = self.repository_manager.get_azure_devops_repository(REPOSITORY_NAME)

        if result is None:
            repository = self.repository_manager.create_repository(REPOSITORY_NAME)
            self.assertEqual(repository.name, REPOSITORY_NAME)

    def test_list_repositories(self):
        result = self.repository_manager.list_repositories()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    def test_list_commits(self):
        result = self.repository_manager.list_commits(REPOSITORY_NAME)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
