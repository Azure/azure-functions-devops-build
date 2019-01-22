# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_devops_build_manager.builder.builder_manager import BuilderManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, BUILD_DEFINITION_NAME, POOL_NAME
from ._helpers import get_credentials

BUILD_DEFINITION_NAME_GIT = None

class TestBuilderManager(unittest.TestCase):

    def test_list_definitions(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        builds = builder_manager.list_builds()

    def test_list_builds(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        definitions = builder_manager.list_definitions()

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                     "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_poll_builds(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        build = builder_manager.poll_build(BUILD_DEFINITION_NAME)

    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                     "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_create_definition_and_build(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        definition = builder_manager.create_definition(BUILD_DEFINITION_NAME, POOL_NAME)
        self.assertEqual(definition.name, BUILD_DEFINITION_NAME)
        self.assertEqual(definition.process['yamlFilename'], 'azure-pipelines.yml')
        build = builder_manager.create_build(BUILD_DEFINITION_NAME, POOL_NAME)
    
    @unittest.skipIf(CREATE_DEVOPS_OBJECTS == False,
                     "skipping - set CREATE_DEVOPS_OBJECTS to True if you don't want to skip creates")
    def test_github_create_definition_and_build(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        definition = builder_manager.create_definition(BUILD_DEFINITION_NAME_GIT, POOL_NAME, github=True)
        self.assertEqual(definition.name, BUILD_DEFINITION_NAME_GIT)
        build = builder_manager.create_build(BUILD_DEFINITION_NAME_GIT, POOL_NAME)

if __name__ == '__main__':
    unittest.main()