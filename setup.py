#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from setuptools import setup, find_packages

NAME = "azure-devops-build-manager"
VERSION = "0.1.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["msrest>=0.2.0", 'mock']

setup(
    name=NAME,
    version=VERSION,
    description="Python package for integrating azure functions with azure devops",
    author_email="t-oldolk@microsoft.com",
    url="https://github.com/dolko/azure-devops-build-manager",
    keywords=["Microsoft", "Azure Devops", "Azure Functions"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)