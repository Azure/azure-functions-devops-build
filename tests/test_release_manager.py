# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.release.release_manager import ReleaseManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, SERVICE_ENDPOINT_NAME, BUILD_DEFINITION_NAME, RELEASE_DEFINITION_NAME, POOL_NAME, FUNCTIONAPP_TYPE, FUNCTIONAPP_NAME, STORAGE_NAME, RESOURCE_GROUP_NAME
from ._helpers import get_credentials


class TestReleaseManager(unittest.TestCase):

    def test_list_release_definitions(self):
        creds = get_credentials()
        release_manager = ReleaseManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        release_manager.list_release_definitions()

    def test_list_releases(self):
        creds = get_credentials()
        release_manager = ReleaseManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        release_manager.list_releases()

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                    "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_basic_release(self):
        creds = get_credentials()
        release_manager = ReleaseManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        release_manager.create_release_definition(PROJECT_NAME, 'drop', "Hosted VS2017", SERVICE_ENDPOINT_NAME, RELEASE_DEFINITION_NAME,
                                                FUNCTIONAPP_TYPE, FUNCTIONAPP_NAME, STORAGE_NAME, RESOURCE_GROUP_NAME)

        release_manager.create_release(RELEASE_DEFINITION_NAME)

    
if __name__ == '__main__':
    unittest.main()