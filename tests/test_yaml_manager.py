# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure_functions_devops_build.yaml.yaml_manager import YamlManager
from ._config import FUNCTIONAPP_LANGUAGE, FUNCTIONAPP_TYPE

class TestYamlManager(unittest.TestCase):

    def test_create_yaml(self):
        yaml_manager = YamlManager(FUNCTIONAPP_LANGUAGE, FUNCTIONAPP_TYPE)
        yaml_manager.create_yaml()
    
if __name__ == '__main__':
    unittest.main()