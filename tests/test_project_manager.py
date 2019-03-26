# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.organization.organization_manager import OrganizationManager
from azure_functions_devops_build.project.project_manager import ProjectManager
from msrest.exceptions import HttpOperationError
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestProjectManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.project_manager = ProjectManager(creds=get_credentials(), organization_name=ORGANIZATION_NAME)

    def tearDown(self):
        self.project_manager.close_connection()

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for testing"
    )
    def test_create_project(self):
        existing_project_names = [
            proj.name for proj in self.project_manager.list_projects().value
        ]

        # If the project exists, we will skip this test
        if PROJECT_NAME in existing_project_names:
            return

        result = self.project_manager.create_project(PROJECT_NAME)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.name, PROJECT_NAME)

    def test_invalid_create_duplicated_project(self):
        existing_project_names = [
            proj.name for proj in self.project_manager.list_projects().value
        ]

        # If no project exists, we will skip this test
        if len(existing_project_names) == 0:
            return

        result = self.project_manager.create_project(existing_project_names[0])
        self.assertFalse(result.valid)

    def test_invalid_create_project_with_bad_name(self):
        bad_project_name = "invalid-project-name#"
        result = self.project_manager.create_project(bad_project_name)
        self.assertFalse(result.valid)

    def test_list_projects(self):
        projects = self.project_manager.list_projects()
        self.assertIsNotNone(projects)
        self.assertIsNotNone(projects.value)
        self.assertGreaterEqual(projects.count, 0)

if __name__ == '__main__':
    unittest.main()
