from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.yaml.yaml_manager import YamlManager

class TestYamlManager(unittest.TestCase):

    def test_create_yaml(self):

        yaml_manager = YamlManager('node', 'linux_consumption')

        print(yaml_manager.create_yaml('subs', 'subs', 'subs'))
        
    
if __name__ == '__main__':
    unittest.main()