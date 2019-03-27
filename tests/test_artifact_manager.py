# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import unittest
from azure_functions_devops_build.artifact.artifact_manager import ArtifactManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestArtifactManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.artifact_manager = ArtifactManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )

    def test_list_artifacts(self):
        artifacts = self.artifact_manager.list_artifacts(build_id="1")
        if not artifacts:
            raise unittest.SkipTest("The build pipeline has no artifacts")

        # If the user is using the devops build manager to make builds there should only be one artifact
        # called drop as a result of running the builder commands.
        self.assertEqual(artifacts[0].name, 'drop')

    def test_invalid_list_artifacts_negative_build_id(self):
        artifacts = self.artifact_manager.list_artifacts(build_id="-1")
        self.assertEqual(len(artifacts), 0)

    def test_invalid_list_artifacts_str_build_id(self):
        with self.assertRaises(TypeError):
            artifacts = self.artifact_manager.list_artifacts(build_id="bad_id")
