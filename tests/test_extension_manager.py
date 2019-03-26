# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.extension.extension_manager import ExtensionManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestExtensionManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.extension_manager = ExtensionManager(organization_name=ORGANIZATION_NAME, creds=get_credentials())

    def test_list_extensions(self):
        extensions = self.extension_manager.list_extensions()
        self.assertIsNotNone(extensions)
        self.assertGreaterEqual(len(extensions), 0)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for unit testing"
    )
    def test_create_extension(self):
        new_extension = self.extension_manager.create_extension('AzureAppServiceSetAppSettings', 'hboelman')
        self.assertTrue(new_extension.publisher_id == 'hboelman')
        self.assertTrue(new_extension.extension_id == 'AzureAppServiceSetAppSettings')

if __name__ == '__main__':
    unittest.main()
