# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_devops_build_manager.extension.extension_manager import ExtensionManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestExtensionManager(unittest.TestCase):

    def test_list_extensions(self):
        creds = get_credentials()
        extension_manager = ExtensionManager(organization_name=ORGANIZATION_NAME, creds=creds)
        extensions = extension_manager.list_extensions()
        self.assertTrue(type(extensions) == list)
    
    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                     "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_create_extension(self):
        creds = get_credentials()
        extension_manager = ExtensionManager(organization_name=ORGANIZATION_NAME, creds=creds)
        new_extension = extension_manager.create_extension('AzureAppServiceSetAppSettings', 'hboelman')
        self.assertTrue(new_extension.publisher_id == 'hboelman')
        self.assertTrue(new_extension.extension_id == 'AzureAppServiceSetAppSettings')
        new_extension = extension_manager.create_extension('PascalNaber-Xpirit-CreateSasToken', 'pascalnaber')
        
if __name__ == '__main__':
    unittest.main()