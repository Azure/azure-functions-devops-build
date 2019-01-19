# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os.path as path
import logging
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from azure_devops_build_manager.constants import (LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS, PYTHON, NODE, NET, JAVA)

class YamlManager(object):
    """ Generate yaml files for devops

    Attributes:
        language: the language of the functionapp you are creating
        app_type: the type of functionapp that you are creating
    """

    def __init__(self, language, app_type):
        """Inits YamlManager as to be able generate the yaml files easily"""
        self._language = language
        self._app_type = app_type

    def create_yaml(self):
        """Create the yaml to be able to create build in the azure-pipelines.yml file"""
        if self._language == PYTHON:
            language_str = 'python'
            dependencies = self._python_dependencies()
        elif self._language == NODE:
            language_str = 'node'
            dependencies = self._node_dependencies()
        elif self._language == NET:
            language_str = 'net'
            dependencies = self._net_dependencies()
        elif self._language == JAVA:
            language_str = 'java'
            dependencies = self._java_dependencies()
            # ADD NEW DEPENDENCIES FOR LANGUAGES HERE
        else:
            logging.warning("valid app type not found")
            dependencies = ""

        if self._app_type == WINDOWS:
            platform_str = 'windows'
            yaml = self._generate_yaml(dependencies, 'VS2017-Win2016', language_str, platform_str)
        else:
            platform_str = 'linux'
            yaml = self._generate_yaml(dependencies, 'ubuntu-16.04', language_str, platform_str)

        with open('azure-pipelines.yml', 'w') as f:
            f.write(yaml)

    def _generate_yaml(self, dependencies, vmImage, language_str, platform_str):
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        template = env.get_template('build.jinja')
        outputText = template.render(dependencies=dependencies, vmImage=vmImage, language=language_str, platform=platform_str)
        return outputText

    def _requires_extensions(self):
        return True if path.exists('extensions.csproj') else False

    def _python_dependencies(self):
        """Helper to create the standard python dependencies"""
        dependencies = []
        dependencies.append('- task: UsePythonVersion@0')
        dependencies.append('  displayName: "Setting python version to 3.6 as required by functions"')
        dependencies.append('  inputs:')
        dependencies.append('    versionSpec: \'3.6\'')
        dependencies.append('    architecture: \'x64\'')
        dependencies.append('- script: |')
        if self._requires_extensions():
            # We need to add the dependencies for the extensions if the functionapp has them
            dependencies.append('    dotnet restore')
            dependencies.append('    dotnet build --runtime ubuntu.16.04-x64 --output \'./bin/\'')
        dependencies.append('    python3.6 -m venv worker_venv')
        dependencies.append('    source worker_venv/bin/activate')
        dependencies.append('    pip3.6 install setuptools')
        dependencies.append('    pip3.6 install -r requirements.txt')
        return dependencies

    def _node_dependencies(self):
        """Helper to create the standard node dependencies"""
        dependencies = []
        dependencies.append('- script: |')
        if self._requires_extensions():
            dependencies.append('    dotnet restore')
            dependencies.append('    dotnet build --output \'./bin/\'')
        dependencies.append('    npm install')
        dependencies.append('    npm run build')
        return dependencies

    def _net_dependencies(self):
        """Helper to create the standard net dependencies"""
        dependencies = []
        dependencies.append('- script: |')
        dependencies.append('    dotnet restore')
        dependencies.append('    dotnet build --output \'./bin/\'')
        return dependencies

    def _java_dependencies(self):
        """Helper to create the standard java dependencies"""
        dependencies = ['- script: |', '    dotnet restore', '    dotnet build', '   mvn clean deploy']
        logging.critical("java dependencies are currently not implemented")
        return dependencies

    def _powershell_dependencies(self):
        # TODO
        exit(1)
