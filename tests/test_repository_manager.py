import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.respository.repository_manager import RepositoryManager

class TestRepositoryManager(unittest.TestCase):

    def test_create_repository(self):
        print("unimplemented")
        
    def test_list_repository(self):
        print("unimplemented")

    def test_get_repository_commits(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = "final-tests-az"
        project_name = "None"
        repository_name = "None"
        repository_manager = RepositoryManager(organization_name=organization_name, project_name=project_name, creds=creds)
        print(repository_manager.get_repository_commits(repository_name))

    
if __name__ == '__main__':
    unittest.main()