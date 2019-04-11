#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from os import path
from setuptools import setup, find_packages

NAME = "azure-functions-devops-build"
VERSION = "0.0.17"

REQUIRES = ["msrest>=0.6.4",
            "vsts>=0.1.25",
            "Jinja2>=2.10"]

file_directory = path.abspath(path.dirname(__file__))

with open(path.join(file_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    license="MIT",
    description="Python package for integrating Azure Functions with Azure DevOps. Specifically made for the Azure CLI",
    author="Oliver Dolk, Hanzhang Zeng",
    author_email="t-oldolk@microsoft.com, hazeng@microsoft.com",
    url="https://github.com/Azure/azure-functions-devops-build",
    keywords=["Microsoft", "Azure DevOps", "Azure Functions", "Azure Pipelines"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests", "sample_yaml_builds"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
