# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_devops_build_manager.builder.builder_manager import BuilderManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, BUILD_DEFINITION_NAME, BUILD_DEFINITION_NAME_GIT, POOL_NAME
from ._helpers import get_credentials

class TestBuilderManager(unittest.TestCase):

    @unittest.skip("skipping - remove this if you want to create organizations")
    def test_create_definition(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        definition = builder_manager.create_definition(BUILD_DEFINITION_NAME, POOL_NAME)
        self.assertEqual(definition.name, BUILD_DEFINITION_NAME)
        self.assertEqual(definition.process['yamlFilename'], 'azure-pipelines.yml')

    def test_git_create_definition(self):
        creds = get_credentials()
        builder_manager = BuilderManager(organization_name=ORGANIZATION_NAME, project_name=PROJECT_NAME, repository_name=REPOSITORY_NAME, creds=creds)
        definition = builder_manager.create_definition(BUILD_DEFINITION_NAME_GIT, POOL_NAME, github=True)
        self.assertEqual(definition.name, BUILD_DEFINITION_NAME_GIT)
        build = builder_manager.create_build(BUILD_DEFINITION_NAME_GIT, POOL_NAME)

if __name__ == '__main__':
    unittest.main()