# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.organization.organization_manager import OrganizationManager
from azure_functions_devops_build.user.user_manager import UserManager
from msrest.exceptions import HttpOperationError
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME
from ._helpers import get_credentials, id_generator

class TestOrganizationManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.organization_manager = OrganizationManager(creds=get_credentials())

    def tearDown(self):
        self.organization_manager.close_connection()

    def test_valid_organization_name(self):
        valid_name = "organization-name-" + id_generator(size=3).lower()
        validation = self.organization_manager.validate_organization_name(valid_name)
        self.assertTrue(validation.valid)

    def test_invalid_no_organization_name(self):
        invalid_name = None
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    def test_invalid_empty_organization_name(self):
        invalid_name = ''
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    def test_invalid_organization_name_characters(self):
        invalid_name = 'invalid-organization-name#'
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    def test_invalid_collided_organization_name(self):
        organizations = self.organization_manager.list_organizations()
        if organizations.count > 0:
            existing_name = organizations.value[0].accountName
            validation = self.organization_manager.validate_organization_name(existing_name)
            self.assertFalse(validation.valid)

    def test_list_organizations(self):
        organizations = self.organization_manager.list_organizations()
        self.assertIsNotNone(organizations)
        self.assertIsNotNone(organizations.value)
        self.assertGreaterEqual(organizations.count, 0)

    def test_invalid_organization_without_credential(self):
        no_cred_organization_manager = OrganizationManager(creds=None)
        with self.assertRaises(HttpOperationError):
            no_cred_organization_manager.list_organizations()

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates"
    )
    def test_create_organization(self):
        existing_organization_names = [
            org.accountName for org in self.organization_manager.list_organizations().value
        ]

        # If the organization exists, we will skip this test
        if ORGANIZATION_NAME in existing_organization_names:
            return

        result = self.organization_manager.create_organization('CUS', ORGANIZATION_NAME)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.name, ORGANIZATION_NAME)

    def test_invalid_create_duplicated_organization(self):
        existing_organization_names = [
            org.accountName for org in self.organization_manager.list_organizations().value
        ]

        # If there is no existing organization, we will skip this test
        if existing_organization_names.count == 0:
            return

        organization_name = existing_organization_names[0]
        with self.assertRaises(HttpOperationError):
            self.organization_manager.create_organization('CUS', organization_name)

    def test_list_regions(self):
        regions = self.organization_manager.list_regions()
        self.assertIsNotNone(regions)
        self.assertIsNotNone(regions.value)
        self.assertGreaterEqual(regions.count, 0)

if __name__ == '__main__':
    unittest.main()
