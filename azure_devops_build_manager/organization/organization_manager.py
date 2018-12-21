from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from . import models

class OrganizationManager(object):

    def __init__(self, base_url='https://app.vssps.visualstudio.com', creds=None, create_organization_url='https://app.vsaex.visualstudio.com'):
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
        #need to make a secondary client for the creating organization as it uses a different base url
        self._create_organization_config = Configuration(base_url= create_organization_url)
        self._create_organization_client = ServiceClient(creds, self._create_organization_config)
        #create the deserializer for the models
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        
    # validate an organization name by checking it does not already exist and that it fits name restrictions
    def validate_organization_name(self, organizationName):
        if re.search("[^0-9A-Za-z-]", organizationName):
            return models.ValidateAccountName(valid=False, message="The name supplied contains forbidden characters. Only alphanumeric characters and dashes are allowed")

        #construct url
        url = '/_AzureSpsAccount/ValidateAccountName'

        #construct query parameters
        query_paramters = {}
        query_paramters['accountName'] = organizationName

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'
        
        request = self._client.get(url, params=query_paramters)
        response = self._client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('ValidateAccountName', response)

        return deserialized


    #get what organizations/accounts this user/member is part of
    def get_organizations(self, id):
        #construct url
        url = '/_apis/Commerce/Subscription'

        query_paramters = {}
        query_paramters['memberId'] = id
        query_paramters['includeMSAAccounts'] = True
        query_paramters['queryOnlyOwnerAccounts'] = True
        query_paramters['inlcudeDisabledAccounts'] = False
        query_paramters['providerNamespaceId'] = 'VisualStudioOnline'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'

        request = self._client.get(url, params=query_paramters)
        response = self._client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Organizations', response)

        return deserialized

    def create_organization(self, regionCode, organizationName):
        #construct url
        url = '/_apis/HostAcquisition/collections'

        #construct query parameters
        query_paramters = {}
        query_paramters['collectionName'] = organizationName
        query_paramters['preferredRegion'] = regionCode
        query_paramters['api-version'] = '4.0-preview.1'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'
        header_paramters['Content-Type'] ='application/json'

        #construct the payload
        payload = {}
        payload['VisualStudio.Services.HostResolution.UseCodexDomainForHostCreation'] = 'true'

        request = self._create_organization_client.post(url=url, params=query_paramters, content=payload)
        response = self._create_organization_client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("POST", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Organization', response)

        return deserialized

    def get_regions(self):
        # Construct URL
        url = '/_apis/commerce/regions'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.get(url, headers=header_paramters)
        response = self._client.send(request)

        # Handle Response
        deserialized = None
        if response.status_code not in [200]:
            print("GET", request.url, file=stderr)
            print("response:", response.status_code, file=stderr)
            print(response.text, file=stderr)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Regions', response)

        return deserialized

    def close_connection(self):
        self._client.close()
        self._create_organization_client.close()