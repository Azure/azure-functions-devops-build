# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os.path as path
import logging
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

    def create_yaml(self, functionapp_name, subscription_name, storage_name, include_release=False):
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

        if self._app_type == WINDOWS:
            yaml = self._windows_yaml(dependencies, functionapp_name, subscription_name, include_release)
        elif self._app_type == LINUX_CONSUMPTION:
            if storage_name == "":
                logging.warning("Storage name cannot be none")
            else:
                yaml = self._linux_consumption_yaml(dependencies, functionapp_name,
                                                    storage_name, subscription_name, include_release)
        elif self._app_type == LINUX_DEDICATED:
            yaml = self._linux_dedicated_yaml(dependencies, functionapp_name, subscription_name, include_release)
        else:
            logging.warning("valid app type not found")
            yaml = ""
        with open('azure-pipelines.yml', 'w') as f:
            f.write(yaml)



    def _linux_consumption_yaml(self, dependencies, functionapp_name, storage_name, subscription_name, include_release):
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
                                     functionapp_name=functionapp_name, storage_name=storage_name)
        return outputText

    def _linux_dedicated_yaml(self, dependencies, functionapp_name, subscription_name, include_release):
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
                                     functionapp_name=functionapp_name)
        return outputText

    def _windows_yaml(self, dependencies, functionapp_name, subscription_name, include_release):
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
                                     subscription_name=subscription_name, functionapp_name=functionapp_name)
        return outputText

    def _requires_extensions(self):
        return True if path.exists('.csproj') else False

    def _python_dependencies(self):
        """Helper to create the standard python dependencies"""
        if self._requires_extensions():
            dependencies = ['- script: |', '    dotnet restore',
                            '    dotnet build', '    pip3 install -r requirements.txt']
        else:
            dependencies = ["- script: pip3 install -r requirements.txt"]
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
