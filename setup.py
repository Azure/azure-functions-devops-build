#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from setuptools import setup, find_packages

NAME = "azure-functions-devops-build"
VERSION = "0.0.4"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["msrest>=0.2.0",
            "vsts>=0.1.25",
            "jinja2>=2.10"]

setup(
    name=NAME,
    version=VERSION,
    description="Python package for integrating azure functions with azure devops. Specifically made for the Azure Cli",
    author_email="t-oldolk@microsoft.com",
    url="https://github.com/dolko/azure-devops-build-manager",
    keywords=["Microsoft", "Azure Devops", "Azure Functions"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'azure_functions_devops_build' : ['*.jinja']},
    long_description="""\
    """
)
