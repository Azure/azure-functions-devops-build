# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_devops_build_manager.service_endpoint.service_endpoint_manager import ServiceEndpointManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, SERVICE_ENDPOINT_NAME, CREATE_DEVOPS_OBJECTS
from ._helpers import get_credentials


class TestServiceEndpointManager(unittest.TestCase):
    
    def test_list_service_endpoint(self):
        creds = get_credentials()
        service_endpoint_manager = ServiceEndpointManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        endpoints = service_endpoint_manager.list_service_endpoints()
        found_endpoint = next((endpoint for endpoint in endpoints if endpoint.name == SERVICE_ENDPOINT_NAME), None)
        self.assertTrue(found_endpoint != None)

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                    "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")      
    def test_create_service_endpoint(self):
        creds = get_credentials()
        service_endpoint_manager = ServiceEndpointManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, creds=creds)
        endpoint = service_endpoint_manager.create_service_endpoint(SERVICE_ENDPOINT_NAME)
        
    
if __name__ == '__main__':
    unittest.main()