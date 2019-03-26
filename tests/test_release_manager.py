# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.release.release_manager import ReleaseManager
from azure_functions_devops_build.service_endpoint.service_endpoint_manager import ServiceEndpointManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, FUNCTIONAPP_TYPE, FUNCTIONAPP_NAME, STORAGE_NAME, RESOURCE_GROUP_NAME
from ._helpers import get_credentials


class TestReleaseManager(unittest.TestCase):
    def setUp(self):
        self._build_definition_name = "_build_{org}_{proj}_{repo}".format(
            org=ORGANIZATION_NAME,
            proj=PROJECT_NAME,
            repo=REPOSITORY_NAME
        )
        self._release_definition_name = "_release_{org}_{proj}_{repo}".format(
            org=ORGANIZATION_NAME,
            proj=PROJECT_NAME,
            repo=REPOSITORY_NAME
        )
        self.release_manager = ReleaseManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )
        self.service_endpoint_manager = ServiceEndpointManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME
        )

    def test_list_release_definitions(self):
        definitions = self.release_manager.list_release_definitions()
        self.assertIsNotNone(definitions)
        self.assertGreaterEqual(len(definitions), 0)

    def test_list_releases(self):
        releases = self.release_manager.list_releases()
        self.assertIsNotNone(releases)
        self.assertGreaterEqual(len(releases), 0)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for unit testing"
    )
    def test_create_release_definition(self):
        service_endpoint_name = self.service_endpoint_manager._get_service_endpoint_name(REPOSITORY_NAME, "pipeline")

        # Skip if service endpoint does not exist
        if service_endpoint_name is None:
            return

        # Skip if release definition already exists
        definitions = self.release_manager.list_release_definitions()
        if self._release_definition_name in [d.name for d in definitions]:
            return

        new_definition = self.release_manager.create_release_definition(
            build_name=self._build_definition_name,
            artifact_name='drop',
            pool_name="Hosted VS2017",
            service_endpoint_name=service_endpoint_name,
            release_definition_name=self._release_definition_name,
            app_type=FUNCTIONAPP_TYPE,
            functionapp_name=FUNCTIONAPP_NAME,
            storage_name=STORAGE_NAME,
            resource_name=RESOURCE_GROUP_NAME
        )
        self.assertIsNotNone(new_definition)
        self.assertEqual(new_definition.name, self._release_definition_name)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for unit testing"
    )
    def test_create_release(self):
        # Skip if release definition does not exist
        definitions = self.release_manager.list_release_definitions()
        if not self._release_definition_name in [d.name for d in definitions]:
            return

        release = self.release_manager.create_release(self._release_definition_name)
        self.assertIsNotNone(release)


if __name__ == '__main__':
    unittest.main()
