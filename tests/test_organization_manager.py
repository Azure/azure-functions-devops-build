# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest, string, random
from azure_functions_devops_build.organization.organization_manager import OrganizationManager
from azure_functions_devops_build.user.user_manager import UserManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME
from ._helpers import get_credentials

class TestOrganizationManager(unittest.TestCase):

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def test_invalid_organization_name_characters(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('hello_123##')
        self.assertFalse(validation.valid)
        organization_manager.close_connection()


    def test_invalid_organization_name_already_exists(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('hello')
        self.assertFalse(validation.valid)
        organization_manager.close_connection()


    def test_valid_organization_name(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('iamatruelykeenbeans')
        self.assertTrue(validation.valid)
        organization_manager.close_connection()

    def test_regions(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        regions = organization_manager.list_regions()
        self.assertEqual(regions.count, len(regions.value))
        organization_manager.close_connection()

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                    "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_create_organization(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(creds=creds)
        regions = organization_manager.list_regions()
        org = organization_manager.create_organization('CUS', ORGANIZATION_NAME)
        organization_manager.close_connection()

    def test_list_organizations(self):
        creds = get_credentials()
        organization_manager = OrganizationManager(creds=creds)
        organizations = organization_manager.list_organizations()
        self.assertTrue(len(organizations.value), organizations.count)
        for val in (organizations.value):
            print(val.accountName)
        #found_organization = next((organization for organization in organizations.value if organization.accountName == ORGANIZATION_NAME), None)
        #self.assertTrue(found_organization != None)
    
if __name__ == '__main__':
    unittest.main()