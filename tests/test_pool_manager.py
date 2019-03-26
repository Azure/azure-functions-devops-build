# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.pool.pool_manager import PoolManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestPoolManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.pool_manager = PoolManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )

    def tearDown(self):
        self.pool_manager.close_connection()

    def test_list_pools(self):
        pools = self.pool_manager.list_pools()
        self.assertIsNotNone(pools)
        self.assertIsNotNone(pools.value)
        self.assertGreaterEqual(pools.count, 0)

if __name__ == '__main__':
    unittest.main()
