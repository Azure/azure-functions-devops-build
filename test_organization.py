import unittest, string, random
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from src.organization.organization import Organization
from src.organization.models.region_details import RegionDetails



class TestOrganization(unittest.TestCase):

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def test_invalid_organization_name_characters(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)
        organization = Organization(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization.validate_organization_name('hello_123##')
        self.assertFalse(validation.valid)


    def test_invalid_organization_name_already_exists(self):
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization = Organization(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization.validate_organization_name('hello')
        self.assertFalse(validation.valid)


    def test_valid_organization_name(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization = Organization(base_url='https://app.vssps.visualstudio.com', creds=creds)
        validation = organization.validate_organization_name('iamatruelykeenbeans')
        self.assertTrue(validation.valid)

    def test_regions(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        organization = Organization(base_url='https://app.vssps.visualstudio.com', creds=creds)
        regions = organization.get_regions()
        
        self.assertEqual(regions.count, 7)

    def test_create_get_organization(self):
        #construct the cli_ctx to auth
        cli_ctx = get_default_cli()
        profile = Profile(cli_ctx=cli_ctx)
        creds, _, _ = profile.get_login_credentials(subscription_id=None)

        name = self.id_generator()





if __name__ == '__main__':
    unittest.main()