# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest
from .test_artifact_manager import TestArtifactManager
from .test_builder_manager import TestBuilderManager
from .test_extension_manager import TestExtensionManager
from .test_organization_manager import TestOrganizationManager
from .test_pool_manager import TestPoolManager
from .test_project_manager import TestProjectManager
from .test_release_manager import TestReleaseManager
from .test_repository_manager import TestRepositoryManager
from .test_service_endpoint_manager import TestServiceEndpointManager
from .test_yaml_manager import TestYamlManager

# TODO : Github integration test suite

def suite():
    suite = unittest.TestSuite()
    
    # We need to make sure we are in the test application's folder that we created to try do these end to end tests
    test_folder = (os.getcwd() + '\python_test_application')
    os.chdir(test_folder)

    # Test the relevant elements of the organization manager
    suite.addTest(TestOrganizationManager('test_invalid_organization_name_characters'))
    suite.addTest(TestOrganizationManager('test_invalid_organization_name_already_exists'))
    suite.addTest(TestOrganizationManager('test_valid_organization_name'))
    suite.addTest(TestOrganizationManager('test_regions'))
    suite.addTest(TestOrganizationManager('test_create_organization'))
    suite.addTest(TestOrganizationManager('test_list_organizations'))
    
    # Test the relevant elements of the project manager
    suite.addTest(TestProjectManager('test_list_projects'))
    suite.addTest(TestProjectManager('test_create_project'))

    # Test the yaml manager
    suite.addTest(TestYamlManager('test_create_yaml'))

    # Test the repository manager
    suite.addTest(TestRepositoryManager('test_list_commits'))
    suite.addTest(TestRepositoryManager('test_list_repositories'))
    suite.addTest(TestRepositoryManager('test_initial_setup'))

    # Test the service endpoint
    suite.addTest(TestServiceEndpointManager('test_create_service_endpoint'))
    suite.addTest(TestServiceEndpointManager('test_list_service_endpoint'))

    # Test the extensions
    suite.addTest(TestExtensionManager('test_create_extension'))
    suite.addTest(TestExtensionManager('test_list_extensions'))

    # Test the builder
    suite.addTest(TestBuilderManager('test_list_definitions'))
    suite.addTest(TestBuilderManager('test_list_builds'))
    suite.addTest(TestBuilderManager('test_create_definition_and_build'))
    suite.addTest(TestBuilderManager('test_poll_builds'))

    # Test the releaser
    suite.addTest(TestReleaseManager('test_list_release_definitions'))
    suite.addTest(TestReleaseManager('test_list_releases'))
    suite.addTest(TestReleaseManager('test_basic_release'))



    suite.addTest(TestArtifactManager('test_list_artifacts'))
    suite.addTest(TestPoolManager('test_list_pools'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())