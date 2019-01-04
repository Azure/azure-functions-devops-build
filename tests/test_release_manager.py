from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.release.release_manager import ReleaseManager
from azure_devops_build_manager.pool.pool_manager import PoolManager

class TestReleaseManager(unittest.TestCase):

    def test_release_definition(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = "dolk-az-python-dedicated"
        project_name = "therat"
        release_definition_name = "test-2"
        release_manager = ReleaseManager(organization_name=organization_name, project_name=project_name, creds=creds)
        release_manager.create_release_definition(project_name, 'drop', "Hosted VS2017", release_definition_name)

        release_manager.create_release(release_definition_name)

    
if __name__ == '__main__':
    unittest.main()