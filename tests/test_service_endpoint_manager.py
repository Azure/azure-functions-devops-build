# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.service_endpoint.service_endpoint_manager import ServiceEndpointManager
from azure_functions_devops_build.exceptions import RoleAssignmentException
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, CREATE_DEVOPS_OBJECTS
from ._helpers import get_credentials


class TestServiceEndpointManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.service_endpoint_manager = ServiceEndpointManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )

    @unittest.SkipTest
    def test_get_service_endpoints(self):
        endpoints = self.service_endpoint_manager.get_service_endpoints(REPOSITORY_NAME)
        self.assertIsNotNone(endpoints)
        self.assertGreaterEqual(len(endpoints), 0)

    @unittest.SkipTest
    def test_get_service_endpoints_has_existing_endpoint(self):
        expected_endpoint_name = self.service_endpoint_manager._get_service_endpoint_name(REPOSITORY_NAME, "pipeline")
        endpoints = self.service_endpoint_manager.get_service_endpoints(REPOSITORY_NAME)
        if len(endpoints) > 0:
            self.assertEqual(endpoints[0].name, expected_endpoint_name)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for testing"
    )
    def test_create_service_endpoint(self):
        expected_endpoint_name = self.service_endpoint_manager._get_service_endpoint_name(REPOSITORY_NAME, "pipeline")
        existing_endpoints = self.service_endpoint_manager.get_service_endpoints(REPOSITORY_NAME)

        # Skip if endpoint exists
        if len(existing_endpoints) > 0:
            return

        # Skip if role assignment permission is not granted
        try:
            endpoint = self.service_endpoint_manager.create_service_endpoint(expected_endpoint_name)
        except RoleAssignmentException:
            raise unittest.SkipTest("Test operator may not have RoleAssignment/Write permission")

        self.assertIsNotNone(endpoint)
        self.assertEqual(endpoint.name, expected_endpoint_name)

if __name__ == '__main__':
    unittest.main()
