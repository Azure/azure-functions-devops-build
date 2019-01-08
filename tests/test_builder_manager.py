import unittest
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.builder.builder_manager import BuilderManager

class TestBuilderManager(unittest.TestCase):

    def test_list_extensions(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        #TODO(oliver): test this - not sure how
        
if __name__ == '__main__':
    unittest.main()