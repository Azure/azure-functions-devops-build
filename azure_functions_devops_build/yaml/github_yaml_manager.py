# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
from ..repository.github_repository_manager import GithubRepositoryManager
from ..base.base_github_manager import BaseGithubManager
from ..constants import (WINDOWS, PYTHON, NODE, DOTNET)
from ..exceptions import LanguageNotSupportException


class GithubYamlManager(BaseGithubManager):

    def __init__(self, language, app_type, github_pat, github_repository):
        super(GithubYamlManager, self).__init__(pat=github_pat)
        self._github_repo_mgr = GithubRepositoryManager(pat=github_pat)
        self._github_repository = github_repository
        self._language = language
        self._app_type = app_type
        self.jinja_env = Environment(
            loader=PackageLoader('azure_functions_devops_build.yaml', 'templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )

    def create_yaml(self, overwrite=False):
        if self._language == PYTHON:
            language_str = 'python'
            package_route = '$(System.DefaultWorkingDirectory)'
            dependencies = self._python_dependencies()
        elif self._language == NODE:
            language_str = 'node'
            package_route = '$(System.DefaultWorkingDirectory)'
            dependencies = self._node_dependencies()
        elif self._language == DOTNET:
            language_str = 'dotnet'
            package_route = '$(System.DefaultWorkingDirectory)/publish_output/s'
            dependencies = self._dotnet_dependencies()
        else:
            raise LanguageNotSupportException(self._language)

        if self._app_type == WINDOWS:
            platform_str = 'windows'
            yaml = self._generate_yaml(dependencies, 'VS2017-Win2016', language_str, platform_str, package_route)
        else:
            platform_str = 'linux'
            yaml = self._generate_yaml(dependencies, 'ubuntu-16.04', language_str, platform_str, package_route)

        if overwrite:
            return self._overwrite_yaml_file(yaml)
        else:
            return self._commit_yaml_file(yaml)

    def _commit_yaml_file(self, data):
        return self._github_repo_mgr.commit_file(
            repository_fullname=self._github_repository,
            file_path="azure-pipelines.yml",
            file_data=data,
            commit_message="Created azure-pipelines.yml by Azure CLI ({time})".format(
                time=datetime.utcnow().strftime("%Y-%m-%d %X UTC")
            ),
        )

    def _overwrite_yaml_file(self, data):
        sha = self._github_repo_mgr.get_content(
            self._github_repository,
            'azure-pipelines.yml',
            get_metadata=True
        ).get("sha")
        return self._github_repo_mgr.commit_file(
            repository_fullname=self._github_repository,
            file_path="azure-pipelines.yml",
            file_data=data,
            commit_message="Overwritten azure-pipelines.yml by Azure CLI ({time})".format(
                time=datetime.utcnow().strftime("%Y-%m-%d %X UTC")
            ),
            sha=sha
        )

    def _generate_yaml(self, dependencies, vmImage, language_str, platform_str, package_route):
        template = self.jinja_env.get_template('build.jinja')
        outputText = template.render(dependencies=dependencies, vmImage=vmImage,
                                     language=language_str, platform=platform_str,
                                     package_route=package_route)
        return outputText

    def _requires_extensions(self):
        return self._github_repo_mgr.check_github_file(self._github_repository, 'extensions.csproj')

    def _requires_pip(self):
        return self._github_repo_mgr.check_github_file(self._github_repository, 'requirements.txt')

    def _requires_npm(self):
        return self._github_repo_mgr.check_github_file(self._github_repository, 'package.json')

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
        if self._requires_pip():
            dependencies.append('    pip3.6 install -r requirements.txt')
        return dependencies

    def _node_dependencies(self):
        """Helper to create the standard node dependencies"""
        dependencies = []
        dependencies.append('- script: |')
        if self._requires_extensions():
            dependencies.append('    dotnet restore')
            if self._app_type == WINDOWS:
                dependencies.append("    dotnet build --output {bs}'./bin/{bs}'".format(bs="\\"))
            else:
                dependencies.append("    dotnet build --runtime ubuntu.16.04-x64 --output './bin/'")
        if self._requires_npm():
            dependencies.append('    npm install')
            dependencies.append('    npm run build --if-present')
            dependencies.append('    npm prune --production')

        if len(dependencies) == 1:
            return []
        return dependencies

    def _dotnet_dependencies(self):
        """Helper to create the standard dotnet dependencies"""
        dependencies = []
        dependencies.append('- script: |')
        dependencies.append('    dotnet restore')
        dependencies.append('    dotnet build --configuration Release')
        dependencies.append("- task: DotNetCoreCLI@2")
        dependencies.append("  inputs:")
        dependencies.append("    command: publish")
        dependencies.append("    arguments: '--configuration Release --output publish_output'")
        dependencies.append("    projects: '*.csproj'")
        dependencies.append("    publishWebProjects: false")
        dependencies.append("    modifyOutputPath: true")
        dependencies.append("    zipAfterPublish: false")
        return dependencies
