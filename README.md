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

This Python library extensively uses the Azure DevOps REST APIs and Azure Devops Python API. See the [Azure DevOps REST API reference](https://docs.microsoft.com/en-us/rest/api/vsts/?view=vsts-rest-5.0) for details on calling different APIs and https://github.com/Microsoft/azure-devops-python-api for details on the azure-devops-python-api.

## Samples

See samples by looking at tests or viewing the [az-cli functionapp devops-build module](https://github.com/Azure/azure-cli/tree/dev/src/command_modules/azure-cli-appservice/azure/cli/command_modules/appservice).

## Testing

Several things need to be setup before you can run the tests:
1. Signed into the az cli. You can do this by using `az login`.
2. Since this directly deploys to azure functions, [create an azure functions functionapp using the azure portal](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function). Make sure you record the details of the subscription name, project name, application type and storage name.
3. Create a _config.py file with all the needed details in the tests folder. You can follow the tests/_config_example.py file in the tests folder to see what information you need.
4. Run the tests using test.cmd

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
