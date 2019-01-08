from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.release.release_manager import ReleaseManager
from azure_devops_build_manager.pool.pool_manager import PoolManager

LINUX_CONSUMPTION = 0
LINUX_DEDICATED = 1
WINDOWS = 2

class TestReleaseManager(unittest.TestCase):

    def test_release_definition(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = "function-deployments-releases"
        project_name = "py-consump"
        release_definition_name = "test-4"
        release_manager = ReleaseManager(organization_name=organization_name, project_name=project_name, creds=creds)
        release_manager.create_release_definition(project_name, 'drop', "Hosted VS2017", organization_name+project_name, release_definition_name,
                                                LINUX_CONSUMPTION, 'dolk-python-consumption-2', 'dolkpythonconsuacfd', 'dolk-python-consumption-2')

        release_manager.create_release(release_definition_name)

    
if __name__ == '__main__':
    unittest.main()