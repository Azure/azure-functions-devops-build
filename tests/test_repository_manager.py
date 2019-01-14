# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.respository.repository_manager import RepositoryManager
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME


class TestRepositoryManager(unittest.TestCase):

    def test_get_repository_commits(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = ORGANIZATION_NAME
        project_name = PROJECT_NAME
        repository_name = REPOSITORY_NAME
        repository_manager = RepositoryManager(organization_name=organization_name, project_name=project_name, creds=creds)
        print(repository_manager.get_repository_commits(repository_name))

    def test_github(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = ORGANIZATION_NAME
        project_name = PROJECT_NAME
        repository_manager = RepositoryManager(organization_name=organization_name, project_name=project_name, creds=creds)
        print(repository_manager._github())

    def test_get_github(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = ORGANIZATION_NAME
        project_name = PROJECT_NAME
        repository_manager = RepositoryManager(organization_name=organization_name, project_name=project_name, creds=creds)
        for repo in (repository_manager._get_github_repsotories().repositories):
            print(repo)

if __name__ == '__main__':
    unittest.main()