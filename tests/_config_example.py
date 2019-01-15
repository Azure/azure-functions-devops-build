# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""This file contains the configs needed for the tests"""

# You need to fill in the variables with names of the resources you already have
# When you are finished setting the configs then you can run test.cmd

# The create devops objects setting sets whether the test will run create commands. The default is true as false requires that you
# have already created the devops objects
CREATE_DEVOPS_OBJECTS = True

# Specify the name of the devops objects you want to create/have already created (in the case of create devops objects being false)
ORGANIZATION_NAME = '{organization name}'
PROJECT_NAME = 'project'
SERVICE_ENDPOINT_NAME = ORGANIZATION_NAME + PROJECT_NAME
REPOSITORY_NAME = PROJECT_NAME
BUILD_DEFINITION_NAME = PROJECT_NAME
RELEASE_DEFINITION_NAME = 'release'

# These parameters are currently not used in tests
GITHUB_REPOSITORY_NAME = None
BUILD_DEFINITION_NAME_GIT = None

# Do not change this from default.
POOL_NAME = 'Default'

# Specify the details of your azure functions resource
FUNCTIONAPP_NAME = '{functionapp name}'
SUBSCRIPTION_NAME = '{subscription name'
STORAGE_NAME = '{storage name}'
RESOURCE_GROUP_NAME = '{resource group name}'
