import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from src.organization.organization_manager import OrganizationManager
from src.user.user_manager import UserManager
from src.organization.models.region_details import RegionDetails

class TestOrganizationManager(unittest.TestCase):

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def test_invalid_organization_name_characters(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('hello_123##')
        self.assertFalse(validation.valid)

        organization_manager.close_connection()


    def test_invalid_organization_name_already_exists(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('hello')
        self.assertFalse(validation.valid)

        organization_manager.close_connection()


    def test_valid_organization_name(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization_manager.validate_organization_name('iamatruelykeenbeans')
        self.assertTrue(validation.valid)

        organization_manager.close_connection()

    def test_regions(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds)
        regions = organization_manager.get_regions()
        
        self.assertEqual(regions.count, 7)

        organization_manager.close_connection()

    @unittest.skip("skipping - remove this if you want to create organizations")
    def test_create_organization(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        name = self.id_generator()

        organization_manager = OrganizationManager(base_url='https://app.vssps.visualstudio.com', creds=creds, create_organization_url='https://app.vsaex.visualstudio.com')
        regions = organization_manager.get_regions()
        
        organization_manager.create_organization(regions.value[0].regionCode, name)

        #since we have created the organization the name is taken
        validation = organization_manager.validate_organization_name(name)
        self.assertFalse(validation.valid)

        organization_manager.close_connection()

    def test_get_organization(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization_manager = OrganizationManager(creds=creds)
        user_manager = UserManager(creds=creds)

        userid = user_manager.get_user_id()

        self.assertRegex(userid.id, r"^[0-9A-Za-z-]+$")

        organizations = organization_manager.get_organizations(userid.id)

        self.assertTrue(len(organizations.value), organizations.count)
    
if __name__ == '__main__':
    unittest.main()