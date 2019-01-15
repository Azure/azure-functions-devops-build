# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.yaml.yaml_manager import YamlManager
from azure_devops_build_manager.constants import LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS, PYTHON, JAVA, NET, NODE
from ._config import FUNCTIONAPP_NAME, SUBSCRIPTION_NAME, STORAGE_NAME

class TestYamlManager(unittest.TestCase):

    def test_create_yaml(self):
        yaml_manager = YamlManager(PYTHON, LINUX_DEDICATED)
        # We don't usually use the file path but for testing we need to make sure we create the azure pipelines file in the right file
        yaml_manager.create_yaml(file_path="python_test_application/azure-pipelines.yml")
    
if __name__ == '__main__':
    unittest.main()