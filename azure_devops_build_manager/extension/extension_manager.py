
import vsts.service_endpoint.v4_1.models as models
from vsts.vss_connection import VssConnection
import uuid
import datetime
from msrest.serialization import TZ_UTC
from dateutil.relativedelta import relativedelta
import subprocess, json, requests

class ExtensionManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", creds=None):
        self._organization_name = organization_name
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self._organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._extension_management_client = connection.get_client('vsts.extension_management.v4_1.extension_management_client.ExtensionManagementClient')

    def create_extension(self, extension_name, publisher_name):

        extensions = self.list_extensions()

        #test if extension is already installed
        installed = False
        for extension in extensions:
            if (extension.publisher_id == publisher_name) and (extension.extension_id == extension_name):
                installed = True
                break

        if not installed:
            extension = self._extension_management_client.install_extension_by_name(publisher_name, extension_name)

        return extension

    def list_extensions(self):
        return self._extension_management_client.get_installed_extensions()
