from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from shutil import copyfile
import textwrap

class YamlManager(object):

    def __init__(self, language):
        self._language = language
        
    def create_yaml(self):
        if self._language == 'python':
            self.create_python()

    def create_python(self):
        with open('azure-pipelines.yml', 'w') as f:
            yaml = textwrap.dedent("""\
                pool:
                vmImage: ubuntu-16.04

                steps:
                - script: echo Hello, world!
                - task: ArchiveFiles@2
                    displayName: "Archive files"
                    inputs:
                    rootFolderOrFile: "$(System.DefaultWorkingDirectory)"
                    includeRootFolder: false
                    tarCompression: none
                    archiveFile: "$(System.DefaultWorkingDirectory)/build$(Build.BuildId).zip"
                - task: PublishBuildArtifacts@1
                    inputs:
                    PathtoPublish: '$(System.DefaultWorkingDirectory)'
                    name: 'drop'""")

            f.write(yaml)
