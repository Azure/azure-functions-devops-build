from __future__ import print_function
from sys import stderr
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
import re
from . import models
import requests

class Organization(object):

    def __init__(self, base_url=None, creds=None):
        self._config = Configuration(base_url= base_url)
        self._client = ServiceClient(creds, self._config)
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
    def get_organizations(self):
        base_url = 'https://app.vssps.visualstudio.com/_apis/Commerce/Subscription'
        params =    {
                    'memberId': self.user.id,
                    'includeMSAAccounts': True,
                    'queryOnlyOwnerAccounts': False,
                    'inlcudeDisabledAccounts': False,
                    'includeMSAAccounts': True,
                    'providerNamespaceId': 'VisualStudioOnline'
                    }
        print(params)
        headers = {
            'Accept' : 'application/json',
            'Authorization' : 'Bearer ' + self.user.bearerToken
            }
        req = requests.get(base_url, params=params, headers=headers)
        return req.json()

    #create a new account/organization
    #eg. create_new_organization(token, CUS, name)
    def create_organization(self, region, name):
        base_url = 'https://app.vsaex.visualstudio.com/_apis/HostAcquisition/collections'
        params =    {
                    'collectionName': name,
                    'preferredRegion': region,
                    'api-version': '4.0-preview.1'
                    }
        headers = {
                'Accept' : 'application/json',
                'Authorization' : 'Bearer ' + self.user.bearerToken,
                'Content-Type': 'application/json'
                }
        payload = {'VisualStudio.Services.HostResolution.UseCodexDomainForHostCreation': 'true'}
        req = requests.post(base_url, data=payload, params=params, headers=headers)
        return req.json()

    def get_regions(self):
        # Construct URL
        url = '/_apis/commerce/regions'
        # Construct Headers
        headers = {
        'Accept' : 'application/json',
        }

        # Construct and send request
        request = self._client.get(url, headers=headers)
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

        