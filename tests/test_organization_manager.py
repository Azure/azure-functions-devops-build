# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.organization.organization_manager import OrganizationManager
from azure_functions_devops_build.user.user_manager import UserManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME
from ._helpers import get_credentials, id_generator

class TestOrganizationManager(unittest.TestCase):

    def setUp(self):
        self.organization_manager = OrganizationManager(creds=get_credentials())

    def tearDown(self):
        self.organization_manager.close_connection()

    # Tests for OrganizationManager.validate_organization_name()
    @unittest.SkipTest
    def test_valid_organization_name(self):
        valid_name = "organization_name"
        validation = self.organization_manager.validate_organization_name(valid_name)
        self.assertTrue(validation.valid)

    @unittest.SkipTest
    def test_invalid_no_organization_name(self):
        invalid_name = None
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    @unittest.SkipTest
    def test_invalid_empty_organization_name(self):
        invalid_name = ''
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    @unittest.SkipTest
    def test_invalid_organization_name_characters(self):
        invalid_name = 'hello_123##'
        validation = self.organization_manager.validate_organization_name(invalid_name)
        self.assertFalse(validation.valid)

    @unittest.SkipTest
    def test_invalid_collided_organization_name(self):
        organizations = self.organization_manager.list_organizations()
        if organizations.count > 0:
            collided_name = organizations.value.
            print(collided_name)

    # Tests for OrganizationManager.validate_organization_name()
    @unittest.SkipTest
    def test_list_organizations(self):
        organizations = self.organization_manager.list_organizations()
        self.assertIsNotNone(organizations)
        self.assertIsNotNone(organizations.value)
        self.assertGreaterEqual(organizations.count, 0)

if __name__ == '__main__':
    unittest.main()
