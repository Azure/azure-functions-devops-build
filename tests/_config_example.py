# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""This file contains the configs needed for the tests"""

# You need to fill in the variables with names of the resources you already have
# When you are finished setting the configs then you can run test.cmd

# The create devops objects setting sets whether the test will run create commands. The default is false. 
# You need to be careful as
CREATE_DEVOPS_OBJECTS = False

# If the create devops is false you only need to specify the following:



# Specify the name of your already created devops objects
ORGANIZATION_NAME = '{organization name}'
PROJECT_NAME = '{project name}'
REPOSITORY_NAME = '{repository name within the project}'
SERVICE_ENDPOINT_NAME = ORGANIZATION_NAME + PROJECT_NAME
GITHUB_REPOSITORY_NAME = '{github repository name }' # leave this as if if not running the github tests

BUILD_DEFINITION_NAME_GIT = '{build definition name for github test}'
BUILD_DEFINITION_NAME = '{build definition name}'
RELEASE_DEFINITION_NAME = '{release definition name}'

# Do not change this from default.
POOL_NAME = 'Default'

# Specify the details of your azure functions resource
FUNCTIONAPP_NAME = '{functionapp name}'
SUBSCRIPTION_NAME = '{subscription name'
STORAGE_NAME = '{storage name}'
RESOURCE_GROUP_NAME = '{resource group name}'
