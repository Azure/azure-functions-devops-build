# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import json
import logging
import unittest
from azure_functions_devops_build.yaml.yaml_manager import YamlManager
from azure_functions_devops_build.constants import (
    PYTHON,
    NODE,
    DOTNET,
    POWERSHELL,
    LINUX_CONSUMPTION,
    LINUX_DEDICATED,
    WINDOWS
)
from ._helpers import id_generator

class TestYamlManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        TestYamlManager.backup_file("requirements.txt")
        TestYamlManager.backup_file("package.json")

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        TestYamlManager.restore_file("requirements.txt")
        TestYamlManager.restore_file("package.json")

    def setUp(self):
        self._current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        if os.path.isfile("azure-pipelines.yml"):
            os.remove("azure-pipelines.yml")

        if os.path.isfile("requirements.txt"):
            os.remove("requirements.txt")

        if os.path.isfile("package.json"):
            os.remove("package.json")

        if os.path.isfile("extensions.csproj"):
            os.remove("extensions.csproj")

    def test_create_yaml_python_linux(self):
        yaml_manager = YamlManager(language=PYTHON, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "python_linux.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_python_linux_pip(self):
        # Create a temporary requirements.txt
        open("requirements.txt", "a").close()
        yaml_manager = YamlManager(language=PYTHON, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "python_linux_pip.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_dotnet_linux(self):
        yaml_manager = YamlManager(language=DOTNET, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "dotnet_linux.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_dotnet_windows(self):
        yaml_manager = YamlManager(language=DOTNET, app_type=WINDOWS)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "dotnet_windows.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_linux(self):
        yaml_manager = YamlManager(language=NODE, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_linux.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_linux_install(self):
        # Create a temporary requirements.txt
        with open("package.json", "w") as f:
            json.dump(obj={}, fp=f)
        yaml_manager = YamlManager(language=NODE, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_linux_install.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_linux_install_build(self):
        # Create a temporary requirements.txt and make a build script in it
        with open("package.json", "w") as f:
            json.dump(obj={"scripts": {"build": "echo test"}}, fp=f)
        yaml_manager = YamlManager(language=NODE, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_linux_install_build.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_linux_install_build_extensions(self):
        # Create a temporary requirements.txt and make a build script in it
        # Create a temporary extensions.csproj
        with open("package.json", "w") as f:
            json.dump(obj={"scripts": {"build": "echo test"}}, fp=f)
        with open("extensions.csproj", "w") as f:
            f.write('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"></Project>')

        yaml_manager = YamlManager(language=NODE, app_type=LINUX_CONSUMPTION)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_linux_install_build_extensions.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_windows(self):
        yaml_manager = YamlManager(language=NODE, app_type=WINDOWS)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_windows.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_windows_install(self):
        # Create a temporary requirements.txt
        with open("package.json", "w") as f:
            json.dump(obj={}, fp=f)
        yaml_manager = YamlManager(language=NODE, app_type=WINDOWS)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_windows_install.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_windows_install_build(self):
        # Create a temporary requirements.txt and make a build script in it
        with open("package.json", "w") as f:
            json.dump(obj={"scripts": {"build": "echo test"}}, fp=f)
        yaml_manager = YamlManager(language=NODE, app_type=WINDOWS)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_windows_install_build.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_node_windows_install_build_extensions(self):
        # Create a temporary requirements.txt and make a build script in it
        # Create a temporary extensions.csproj
        with open("package.json", "w") as f:
            json.dump(obj={"scripts": {"build": "echo test"}}, fp=f)
        with open("extensions.csproj", "w") as f:
            f.write('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"></Project>')

        yaml_manager = YamlManager(language=NODE, app_type=WINDOWS)
        yaml_manager.create_yaml()

        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "node_windows_install_build_extensions.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_powershell_windows(self):
        yaml_manager = YamlManager(language=POWERSHELL, app_type=WINDOWS)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "powershell_windows.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    def test_create_yaml_powershell_windows_extensions(self):
        # Create a temporary extensions.csproj
        with open("extensions.csproj", "w") as f:
            f.write('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"></Project>')

        yaml_manager = YamlManager(language=POWERSHELL, app_type=WINDOWS)
        yaml_manager.create_yaml()
        yaml_path = os.path.join(self._current_directory, "pipeline_scripts", "powershell_windows_extensions.yml")
        result = TestYamlManager.is_two_files_equal("azure-pipelines.yml", yaml_path)
        self.assertTrue(result)

    @staticmethod
    def is_two_files_equal(filepath1, filepath2):
        with open(filepath1, "r") as f1:
            content1 = f1.read()
        with open(filepath2, "r") as f2:
            content2 = f2.read()
        return content1 == content2

    @staticmethod
    def backup_file(filepath):
        backup_filepath = "{}.bak".format(filepath)
        if os.path.isfile(filepath):
            if os.path.isfile(backup_filepath):
                os.remove(backup_filepath)
            os.rename(filepath, backup_filepath)

    @staticmethod
    def restore_file(filepath):
        backup_filepath = "{}.bak".format(filepath)
        if os.path.isfile(backup_filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
            os.rename(backup_filepath, filepath)

if __name__ == '__main__':
    unittest.main()
