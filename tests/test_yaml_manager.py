from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.yaml.yaml_manager import YamlManager
from azure_devops_build_manager.constants import LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS, PYTHON, JAVA, NET, NODE

class TestYamlManager(unittest.TestCase):

    def test_create_yaml(self):

        yaml_manager = YamlManager(JAVA, WINDOWS)

        print(yaml_manager.create_yaml("{functionapp_name}", "{subscription_name}", "{storage_name}", True))
        
    
if __name__ == '__main__':
    unittest.main()