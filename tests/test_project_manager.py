# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.project.project_manager import ProjectManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestProjectManager(unittest.TestCase):

    def test_list_projects(self):
        creds = get_credentials()
        project_manager = ProjectManager(organization_name=ORGANIZATION_NAME, creds=creds)
        projects = project_manager.list_projects()
        self.assertEqual(projects.count, len(projects.value))

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")       
    def test_create_project(self):
        creds = get_credentials()
        project_manager = ProjectManager(organization_name=ORGANIZATION_NAME, creds=creds)
        p = project_manager.create_project(PROJECT_NAME)

    
if __name__ == '__main__':
    unittest.main()