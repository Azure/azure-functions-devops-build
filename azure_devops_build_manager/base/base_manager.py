# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from vsts.vss_connection import VssConnection

class BaseManager(object):
    """ 
    The basic manager which the other classes are build on

    Attributes:
        organization_name : The name of the DevOps organization
        project_name : The name of the DevOps project
        creds : These are credentials for an Azure user
    """
    def __init__(self, organization_name, project_name, creds, repository_name=""):
        self._organization_name = organization_name
        self._project_name = project_name
        self._creds = creds
        self._repository_name = repository_name
        self._connection = VssConnection(base_url='https://dev.azure.com/' + organization_name, creds=creds)