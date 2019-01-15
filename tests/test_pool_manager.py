# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.pool.pool_manager import PoolManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestPoolManager(unittest.TestCase):

    def test_list_pools(self):
        creds = get_credentials()
        pool_manager = PoolManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        pools = (pool_manager.list_pools())
        self.assertTrue(len(pools.value), pools.count)
        pool_manager.close_connection()

if __name__ == '__main__':
    unittest.main()