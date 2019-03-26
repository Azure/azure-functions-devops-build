# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import shutil
import logging
import unittest
from azure_functions_devops_build.repository.repository_manager import RepositoryManager
from azure_functions_devops_build.repository.local_git_utils import (
    does_git_exist,
    does_local_git_repository_exist,
    does_git_remote_exist,
    git_init,
    git_add_remote
)
from ._config import ORGANIZATION_NAME, PROJECT_NAME, REPOSITORY_NAME, CREATE_DEVOPS_OBJECTS
from ._helpers import get_credentials

_git_exist = does_git_exist()

class TestRepositoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        cls.backup_git_context()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        cls.restore_git_context()

    def setUp(self):
        self.repository_manager = RepositoryManager(
            organization_name=ORGANIZATION_NAME,
            project_name=PROJECT_NAME,
            creds=get_credentials()
        )

    def tearDown(self):
        if os.path.exists(".git"):
            shutil.rmtree(".git", ignore_errors=True)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git(self):
        result = RepositoryManager.check_git()
        self.assertTrue(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_local_repository_not_exist(self):
        result = RepositoryManager.check_git_local_repository()
        self.assertFalse(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_local_repository_exist(self):
        git_init()
        result = RepositoryManager.check_git_local_repository()
        self.assertTrue(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_remote_not_exist_no_repo(self):
        result = self.repository_manager.check_git_remote(REPOSITORY_NAME, "azuredevops")
        self.assertFalse(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_remote_not_exist_no_remote(self):
        git_init()
        result = self.repository_manager.check_git_remote(REPOSITORY_NAME, "azuredevops")
        self.assertFalse(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_remote_not_exist_wrong_remote(self):
        git_init()
        git_add_remote("random_remote", "https://random.com/url")
        result = self.repository_manager.check_git_remote(REPOSITORY_NAME, "azuredevops")
        self.assertFalse(result)

    @unittest.skipIf(not _git_exist, "git does not exist")
    def test_check_git_remote_exist(self):
        git_init()
        git_add_remote(
            "_azuredevops_{org}_{proj}_{repo}".format(
                org=ORGANIZATION_NAME,
                proj=PROJECT_NAME,
                repo=REPOSITORY_NAME
            ),
            "https://dev.azure.com/{org}/{proj}/_git/{repo}".format(
                org=ORGANIZATION_NAME,
                proj=PROJECT_NAME,
                repo=REPOSITORY_NAME
            )
        )
        result = self.repository_manager.check_git_remote(REPOSITORY_NAME, "azuredevops")
        self.assertTrue(result)

    def test_get_repo_branches(self):
        result = self.repository_manager.get_azure_devops_repository_branches(REPOSITORY_NAME)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    def test_get_repo(self):
        result = self.repository_manager.get_azure_devops_repository(REPOSITORY_NAME)
        if result is not None:
            self.assertEqual(result.name, REPOSITORY_NAME)

    def test_invalid_get_repo_bad_name(self):
        result = self.repository_manager.get_azure_devops_repository("bad@name")
        self.assertIsNone(result)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for testing"
    )
    def test_create_repository(self):
        result = self.repository_manager.get_azure_devops_repository(REPOSITORY_NAME)

        if result is None:
            repository = self.repository_manager.create_repository(REPOSITORY_NAME)
            self.assertEqual(repository.name, REPOSITORY_NAME)

    def test_list_repositories(self):
        result = self.repository_manager.list_repositories()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    def test_list_commits(self):
        result = self.repository_manager.list_commits(REPOSITORY_NAME)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 0)

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for testing"
    )
    def test_setup_local_get_repository_no_git(self):
        self.repository_manager.setup_local_git_repository(REPOSITORY_NAME, "azuredevops")
        self.assertTrue(does_local_git_repository_exist())
        self.assertTrue(does_git_remote_exist(REPOSITORY_NAME))

    @unittest.skipIf(
        not CREATE_DEVOPS_OBJECTS,
        "Set CREATE_DEVOPS_OBJECTS to True if you want to create resources for testing"
    )
    def test_setup_local_get_repository_on_existing_git(self):
        git_init()
        self.repository_manager.setup_local_git_repository(REPOSITORY_NAME, "azuredevops")
        self.assertTrue(does_local_git_repository_exist())
        self.assertTrue(does_git_remote_exist(REPOSITORY_NAME))

    @staticmethod
    def does_git_exist():
        try:
            result = check_call("git", stdout=DEVNULL, stderr=DEVNULL)
        except CalledProcessError as e:
            return e.returncode == 1
        except Exception:
            return False

    @staticmethod
    def backup_git_context():
        if os.path.isdir(".git"):
            shutil.move(".git", ".git.bak")

    @staticmethod
    def restore_git_context():
        if os.path.isdir(".git.bak"):
            shutil.move(".git.bak", ".git")

if __name__ == '__main__':
    unittest.main()
