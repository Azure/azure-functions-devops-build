# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.builder.builder_manager import BuilderManager
from ._config import CREATE_DEVOPS_OBJECTS, ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME
from ._helpers import get_credentials


class TestBuilderManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self._build_definition_name = "_build_{org}_{proj}_{repo}".format(
            org=ORGANIZATION_NAME,
            proj=PROJECT_NAME,
            repo=REPOSITORY_NAME
        )
        self.builder_manager = BuilderManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            repository_name=REPOSITORY_NAME,
            creds=get_credentials()
        )

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for unit testing"
    )
    def test_create_definition(self):
        definitions = self.builder_manager.list_definitions()

        # Skip if definition already exists
        if self._build_definition_name in [d.name for d in definitions]:
            raise unittest.SkipTest("Build definition exists. No need to create a new build definition.")

        definition = self.builder_manager.create_devops_build_definition(self._build_definition_name, "Default")
        self.assertEqual(definition.name, self._build_definition_name)
        self.assertEqual(definition.process['yamlFilename'], 'azure-pipelines.yml')

    def test_list_definitions(self):
        result = self.builder_manager.list_definitions()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    def test_list_builds(self):
        result = self.builder_manager.list_builds()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for unit testing"
    )
    def test_create_build(self):
        result = self.builder_manager.create_build(self._build_definition_name, "Default")
        self.assertIsNotNone(result)
        self.assertEqual(result.definition.name, self._build_definition_name)

if __name__ == '__main__':
    unittest.main()
