# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

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


if __name__ == '__main__':
    unittest.main()
