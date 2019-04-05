#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from setuptools import setup, find_packages

NAME = "azure-functions-devops-build"
VERSION = "0.0.15"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["msrest",
            "vsts",
            "jinja2"]

setup(
    name=NAME,
    version=VERSION,
    description="Python package for integrating Azure Functions with Azure DevOps. Specifically made for the Azure CLI",
    author="Oliver Dolk, Hanzhang Zeng",
    author_email="t-oldolk@microsoft.com, hazeng@microsoft.com",
    url="https://github.com/Azure/azure-functions-devops-build",
    keywords=["Microsoft", "Azure DevOps", "Azure Functions", "Azure Pipelines"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests", "sample_yaml_builds"]),
    include_package_data=True,
    long_description=""
)
