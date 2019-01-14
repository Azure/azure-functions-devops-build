# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.service_endpoint.service_endpoint_manager import ServiceEndpointManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials


class TestServiceEndpointManager(unittest.TestCase):

    def test_create_yaml(self):
        creds = get_credentials()
        service_endpoint_manager = ServiceEndpointManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        endpoints = service_endpoint_manager.list_service_endpoints()
      
    
if __name__ == '__main__':
    unittest.main()