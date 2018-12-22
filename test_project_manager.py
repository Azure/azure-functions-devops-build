from __future__ import print_function

import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.project.project_manager import ProjectManager

class TestProjectManager(unittest.TestCase):

    def test_get_projects(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        project_manager = ProjectManager(organization_name="t-oldolk", creds=creds)
        projects = project_manager.get_existing_projects()

        self.assertTrue(hasattr(projects, 'value'))
        self.assertTrue(hasattr(projects, 'count'))
        
    
if __name__ == '__main__':
    unittest.main()