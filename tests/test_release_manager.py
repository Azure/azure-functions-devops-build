from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.release.release_manager import ReleaseManager
from azure_devops_build_manager.pool.pool_manager import PoolManager

class TestReleaseManager(unittest.TestCase):

    def get_pool(self, organization_name, project_name, creds):
        pool_manager = PoolManager(organization_name=organization_name, project_name=project_name, creds=creds)
        pools = pool_manager.get_pools()
        for pool in pools.value:
            if pool.name == "Hosted VS2017":
                return pool

    def test_release_definition(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = "t-oldolk"
        project_name = "windows_function_app_samples"
        pool = self.get_pool(organization_name, project_name, creds)
        release_manager = ReleaseManager(organization_name=organization_name, project_name=project_name, creds=creds)
        release_manager.create_release_definition('node-functionapp-repo', 'drop', pool)

    
if __name__ == '__main__':
    unittest.main()