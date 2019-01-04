from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from shutil import copyfile
import textwrap
import jinja2
import os
from jinja2 import Environment, PackageLoader, select_autoescape

LINUX_CONSUMPTION = 0
LINUX_DEDICATED = 1
WINDOWS = 2

class YamlManager(object):

    def __init__(self, language, appType):
        self._language = language
        self._appType = appType
        
    def create_yaml(self, functionapp_name, subscription_name, storage_name, include_release=False):
        if self._language == 'python':
            dependencies = self.python_dependencies()
        elif self._language == 'node':
            dependencies = self.node_dependencies()
        else:
            dependencies = ""

        if self._appType == WINDOWS:
            yaml = self.windows_yaml(dependencies, functionapp_name, subscription_name, include_release)
        elif self._appType == LINUX_CONSUMPTION:
            if storage_name == "":
                print("STORAGE NAME CANNOT BE NONE")
            else:
                yaml = self.linux_consumption_yaml(dependencies, functionapp_name, storage_name, subscription_name, include_release)
        elif self._appType == LINUX_DEDICATED:
            yaml = self.linux_dedicated_yaml(dependencies, functionapp_name, subscription_name, include_release)
        else:
            yaml = ""


        with open('azure-pipelines.yml', 'w') as f:
            f.write(yaml)

        return yaml

    def linux_consumption_yaml(self, dependencies, functionapp_name, storage_name, subscription_name, include_release):
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
            template = env.get_template('linux_consumption_release_included.jinja')
        else:
            template = env.get_template('linux_consumption.jinja')
        outputText = template.render(dependencies=dependencies, subscription_name=subscription_name, functionapp_name=functionapp_name, storage_name=storage_name)

        return outputText

    def linux_dedicated_yaml(self, dependencies, functionapp_name, subscription_name, include_release):
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
           template = env.get_template('linux_dedicated_release_included.jinja')
        else: 
            template = env.get_template('linux_dedicated.jinja')
        outputText = template.render(dependencies=dependencies, subscription_name=subscription_name, functionapp_name=functionapp_name)

        return outputText

    def windows_yaml(self, dependencies, functionapp_name, subscription_name, include_release):
        env = Environment(
            loader=PackageLoader('azure_devops_build_manager.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        if include_release:
            template = env.get_template('windows_release_included.jinja')
        else:
            template = env.get_template('windows.jinja')
        outputText = template.render(language=self._language, appType=self._appType, dependencies=dependencies, subscription_name=subscription_name, functionapp_name=functionapp_name)

        return outputText

    def python_dependencies(self):
        dependencies = ["- script: pip3 install -r requirements.txt"]
        return dependencies

    def node_dependencies(self):
        dependencies = ['- script: |', '   npm install', '   npm run build', "  displayName: 'Install dependencies'"]
        return dependencies

    