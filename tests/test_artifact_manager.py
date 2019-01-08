import unittest
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.artifact.artifact_manager import ArtifactManager

class TestArtifactManager(unittest.TestCase):

    def test_list_extensions(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_name = "function-deployments-releases"
        project_name = "blah"
        artifact_manager = ArtifactManager(organization_name=organization_name, project_name=project_name, creds=creds)
        self.assertTrue(type(artifact_manager.list_artifacts("1")) == list)
        
if __name__ == '__main__':
    unittest.main()