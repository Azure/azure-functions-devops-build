# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.pool.pool_manager import PoolManager

class TestPoolManager(unittest.TestCase):

    def test_list_pools(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        pool_manager = PoolManager(organization_name="t-oldolk", project_name="demo", creds=creds)
        pools = (pool_manager.list_pools())
        self.assertTrue(len(pools.value), pools.count)
        pool_manager.close_connection()

if __name__ == '__main__':
    unittest.main()