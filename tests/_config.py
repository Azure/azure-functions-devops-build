# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from azure_functions_devops_build.constants import LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS, NODE, PYTHON, JAVA, DOTNET

"""This file contains the configs needed for the tests"""

# You need to fill in the variables with names of the resources you already have
# When you are finished setting the configs then you can run test.cmd

# The create devops objects setting sets whether the test will run create commands. The default is true as false requires that you
# have already created the devops objects
CREATE_DEVOPS_OBJECTS = True

# Specify the name of the devops objects you want to create/have already created (in the case of create devops objects being false)
ORGANIZATION_NAME = 'hz-org'
PROJECT_NAME = 'hz-proj-test'
REPOSITORY_NAME = 'hz-repo-test'

# Do not change this from default.
POOL_NAME = 'Default'

# Specify the details of your azure functions resource
FUNCTIONAPP_NAME = 'hazeng-function-test'
STORAGE_NAME = 'hazengfunctiontbd8d'
RESOURCE_GROUP_NAME = 'hazeng-function-linux'
FUNCTIONAPP_TYPE = 'LINUX_CONSUMPTION' # choose from LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS
FUNCTIONAPP_LANGUAGE = 'PYTHON' # choose from NODE, PYTHON, JAVA, DOTNET
