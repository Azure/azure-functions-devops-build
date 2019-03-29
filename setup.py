#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from setuptools import setup, find_packages

NAME = "azure-functions-devops-build"
VERSION = "0.0.13"

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
    description="Python package for integrating azure functions with azure devops. Specifically made for the Azure Cli",
    author_email="t-oldolk@microsoft.com",
    url="https://github.com/Azure/azure-functions-devops-build",
    keywords=["Microsoft", "Azure Devops", "Azure Functions"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    long_description="""\
    """
)
