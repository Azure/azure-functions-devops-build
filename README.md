# Azure Devops Build Manager For Azure Functions (Under Development)

This project provides the class AzureDevopsBuildManager and supporting classes. This manager class allows
the caller to manage Azure Devops pipelines that are maintained within an Azure Devops account.

## Install
```
pip install adbm
```
## Get started
To use the API, you need to first establish a connection to azure by loging into your azure account using `az login`. You can then follow the example as below. Firstly we get the token from login and use this to authenticate the different python function calls.

```python
from azure.cli.core import get_default_cli
from azure.cli.core._profile import Profile
from azure_devops_build_manager.organization.organization_manager import OrganizationManager
import pprint

# Get your token from the az login cache
cli_ctx = get_default_cli()
profile = Profile(cli_ctx=cli_ctx)
creds, _, _ = profile.get_login_credentials(subscription_id=None)

# Create an organization manager and user manager using your credentials
organization_manager = OrganizationManager(creds=creds)
user_manager = UserManager(creds=creds)

# Get your user id
userid = user_manager.get_user_id()

# Get the list of organizations for your user
organizations = organization_manager.get_organizations(userid.id)

# Show details about each organization in the console
for organization in organizations:
    pprint.pprint(organization.__dict__)
```

## API documentation

This Python library extensively uses the Azure DevOps REST APIs and Azure Devops Python API. See the [Azure DevOps REST API reference](https://docs.microsoft.com/en-us/rest/api/vsts/?view=vsts-rest-5.0) for details on calling different APIs and [Azure DevOps Python SDK] (https://github.com/Microsoft/azure-devops-python-api) for details on the azure-devops-python-api.

## Samples

See samples by looking at tests or viewing the az-cli functionapp devops-build module.

## Testing

Several things need to be setup before you can run the tests:



To run the tests you need to first setup the config file in the tests file. Follow the instructions in there and then run `python -m unittest discover`

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
