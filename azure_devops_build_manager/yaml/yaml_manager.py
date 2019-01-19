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

    def create_yaml(self, functionapp_name=None, subscription_name=None, storage_name=None, resource_group_name=None, include_release=False, file_path="", settings=[]):
        """Create the yaml to be able to create build in the azure-pipelines.yml file"""
        if self._language == PYTHON:
            dependencies = self._python_dependencies()
        elif self._language == NODE:
            dependencies = self._node_dependencies()
        elif self._language == NET:
            dependencies = self._net_dependencies()
        elif self._language == JAVA:
            dependencies = self._java_dependencies()
        else:
            logging.warning("valid app type not found")
            dependencies = ""

        # Disable the settings at the moment until it is resolved ...
        settings = []

        if self._app_type == WINDOWS:
            yaml = self._windows_yaml(dependencies, functionapp_name, subscription_name, resource_group_name, include_release, settings)
        elif self._app_type == LINUX_CONSUMPTION:
            if storage_name == "":
                logging.warning("Storage name cannot be none")
            else:
                yaml = self._linux_consumption_yaml(dependencies, functionapp_name,
                                                    storage_name, subscription_name, resource_group_name, include_release, settings)
        elif self._app_type == LINUX_DEDICATED:
            yaml = self._linux_dedicated_yaml(dependencies, functionapp_name, subscription_name, resource_group_name, include_release, settings)
        else:
            logging.warning("valid app type not found")
            yaml = ""

        # User can specify the file path
        if file_path != "":
            with open(file_path, 'w') as f:
                f.write(yaml)
        else:
            with open('azure-pipelines.yml', 'w') as f:
                f.write(yaml)

    def _linux_consumption_yaml(self, dependencies, functionapp_name, storage_name, subscription_name, resource_group_name, include_release, settings):
        """Helper to create the yaml for linux consumption"""
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
            template = env.get_template('linux_consumption_release_included.jinja')
        else:
            template = env.get_template('linux_consumption.jinja')

        outputText = template.render(dependencies=dependencies, subscription_name=subscription_name,
                                     functionapp_name=functionapp_name, storage_name=storage_name, resource_group_name=resource_group_name, settings=settings)
        return outputText

    def _linux_dedicated_yaml(self, dependencies, functionapp_name, subscription_name, resource_group_name, include_release, settings):
        """Helper to create the yaml for linux dedicated"""
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
            template = env.get_template('linux_dedicated_release_included.jinja')
        else:
            template = env.get_template('linux_dedicated.jinja')
        outputText = template.render(dependencies=dependencies, subscription_name=subscription_name,
                                     functionapp_name=functionapp_name, resource_group_name=resource_group_name, settings=settings)
        return outputText

    def _windows_yaml(self, dependencies, functionapp_name, subscription_name, resource_group_name, include_release, settings):
        """Helper to create the yaml for windows"""
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
            template = env.get_template('windows_release_included.jinja')
        else:
            template = env.get_template('windows.jinja')
        outputText = template.render(language=self._language, appType=self._app_type, dependencies=dependencies,
                                     subscription_name=subscription_name, functionapp_name=functionapp_name, resource_group_name=resource_group_name,
                                     settings=settings)
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
        if self._requires_extensions():
            dependencies = ['- script: |', '    dotnet restore',
                            '    dotnet build', '    npm install',
                            '    npm run build', "  displayName: 'Install dependencies'"]
        else:
            dependencies = ['- script: |', '    npm install', '    npm run build', "  displayName: 'Install dependencies'"]
        return dependencies

    def _net_dependencies(self):
        """Helper to create the standard net dependencies"""
        dependencies = ['- script: |', '    dotnet restore', '    dotnet build']
        return dependencies

    def _java_dependencies(self):
        """Helper to create the standard java dependencies"""
        dependencies = ['- script: |', '    dotnet restore', '    dotnet build', '   mvn clean deploy']
        logging.critical("java dependencies are currently not implemented")
        return dependencies
