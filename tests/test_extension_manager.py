from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.extension.extension_manager import ExtensionManager

class TestExtensionManager(unittest.TestCase):

    def test_list_extensions(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        extension_manager = ExtensionManager(organization_name="t-oldolk", creds=creds)
        extensions = extension_manager.list_extensions()
        self.assertTrue(type(extensions) == list)

    def test_create_extension(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        extension_manager = ExtensionManager(organization_name="t-oldolk", creds=creds)
        new_extension = extension_manager.create_extension('AzureAppServiceSetAppSettings', 'hboelman')
        self.assertTrue(new_extension.publisher_id == 'hboelman')
        self.assertTrue(new_extension.extension_id == 'AzureAppServiceSetAppSettings')
        
if __name__ == '__main__':
    unittest.main()