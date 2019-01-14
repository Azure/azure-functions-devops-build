# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.release.release_manager import ReleaseManager
from azure_devops_build_manager.pool.pool_manager import PoolManager
from azure_devops_build_manager.constants import LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS
from ._helpers import get_credentials


class TestReleaseManager(unittest.TestCase):

    def test_basic_release(self):
        creds = get_credentials()
        organization_name = "function-deployments-releases"
        project_name = "py-consump"
        release_definition_name = "test-4"
        release_manager = ReleaseManager(organization_name=organization_name, project_name=project_name, creds=creds)
        release_manager.create_release_definition(project_name, 'drop', "Hosted VS2017", organization_name+project_name, release_definition_name,
                                                LINUX_CONSUMPTION, 'dolk-python-consumption-2', 'dolkpythonconsuacfd', 'dolk-python-consumption-2')

        release_manager.create_release(release_definition_name)

    
if __name__ == '__main__':
    unittest.main()