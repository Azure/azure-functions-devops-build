# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock

import vsts
from vsts.build.v4_1.models.build_artifact import BuildArtifact
import azure_devops_build_manager
from azure_devops_build_manager.artifact.artifact_manager import ArtifactManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME
from ._helpers import get_credentials

from vsts.core.v4_1.models.team_project_reference import TeamProjectReference

class TestArtifactManager(unittest.TestCase):

    def test_list_artifacts(self):
        creds = get_credentials()
        organization_name = ORGANIZATION_NAME
        project_name = PROJECT_NAME
        artifact_manager = ArtifactManager(organization_name=organization_name, project_name=project_name, creds=creds)
        artifacts = artifact_manager.list_artifacts("1")
        if artifacts:
            # There should only be one artifact as a result of the operation called drop
            self.assertEqual(artifacts[0].name, 'drop')
        
if __name__ == '__main__':
    unittest.main()