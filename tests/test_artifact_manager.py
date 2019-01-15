# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_devops_build_manager.artifact.artifact_manager import ArtifactManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

class TestArtifactManager(unittest.TestCase):

    def test_list_artifacts(self):
        """This test tests the functionality of listing artifacts. It requires there to be artifacts to list in the project"""
        creds = get_credentials()
        organization_name = ORGANIZATION_NAME
        project_name = PROJECT_NAME
        artifact_manager = ArtifactManager(organization_name=organization_name, project_name=project_name, creds=creds)
        artifacts = artifact_manager.list_artifacts("1")
        if artifacts:
            # If the user is using the devops build manager to make builds there should only be one artifact 
            # called drop as a result of running the builder commands.
            self.assertEqual(artifacts[0].name, 'drop')
