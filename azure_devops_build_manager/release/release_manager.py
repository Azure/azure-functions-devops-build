from vsts.vss_connection import VssConnection
import uuid
import datetime
from msrest.serialization import TZ_UTC
from dateutil.relativedelta import relativedelta
import subprocess, json, requests
import vsts.release.v4_1.models as models


class ReleaseManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", project_name="", creds=None):
        self._organization_name = organization_name
        self._project_name = project_name
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self._organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._agent_client = connection.get_client("vsts.task_agent.v4_1.task_agent_client.TaskAgentClient")
        self._build_client = connection.get_client('vsts.build.v4_1.build_client.BuildClient')
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._release_client = connection.get_client('vsts.release.v4_1.release_client.ReleaseClient')

    def create_release_definition(self, build_name, artifact_name):
        project = self.get_project_by_name(self._project_name)
        build = self.get_build_by_name(project, build_name)
        retention_policy_environment = self.get_retention_policy()
        artifact = self.get_artifact(build, project, artifact_name)

        # release_deploy_step = models.release_definition_deploy_step.ReleaseDefinitionDeployStep(
        #     id=2
        # )

        pre_approval = models.release_definition_approval_step.ReleaseDefinitionApprovalStep(
            id = 22,
            rank = 1,
            is_automated = True,
            is_notification_on = False
        )

        post_approval = models.release_definition_approval_step.ReleaseDefinitionApprovalStep(
            id = 24,
            rank = 1,
            is_automated = True,
            is_notification_on = False
        )


        pre_release_approvals = models.release_definition_approvals.ReleaseDefinitionApprovals(
            approvals=[pre_approval]
        )

        post_release_approvals = models.release_definition_approvals.ReleaseDefinitionApprovals(
            approvals=[post_approval]
        )

        deploy_phases = [
                    {
                        "deploymentInput": {
                            "parallelExecution": {
                                "parallelExecutionType": 0
                            },
                            "skipArtifactsDownload": False,
                            "artifactsDownloadInput": {
                                "downloadInputs": [
                                    {
                                        "artifactItems": [],
                                        "alias": self.build.name,
                                        "artifactType": "Build",
                                        "artifactDownloadMode": "All"
                                    }
                                ]
                            },
                            "queueId": self.build.poolid,
                            "demands": [],
                            "enableAccessToken": False,
                            "timeoutInMinutes": 0,
                            "jobCancelTimeoutInMinutes": 1,
                            "condition": "succeeded()",
                            "overrideInputs": {},
                            "dependencies": []
                        },
                        "rank": 1,
                        "phaseType": 1,
                        "name": "Agent job",
                        "refName": None,
                        "workflowTasks": [
                            {
                                "name": "AzureBlob File Copy",
                                "refName": "",
                                "enabled": True,
                                "timeoutInMinutes": 0,
                                "inputs": {
                                    "SourcePath": "$(System.DefaultWorkingDirectory)/" + self.build.name + "/drop/build$(Build.BuildId).zip",
                                    "ConnectedServiceNameSelector": "ConnectedServiceNameARM",
                                    "ConnectedServiceName": "",
                                    "ConnectedServiceNameARM": "b96bc246-5aef-4abd-8a6c-73f5113bacb1", #self.service_endpoint.endpoint.id,    #"3765b613-bcbb-433b-9971-09a76371193c",
                                    "Destination": "AzureBlob",
                                    "StorageAccount": "",
                                    "StorageAccountRM": self.resource.storage['name'], #"dolkpythonappse9cae", #may need to replace this
                                    "ContainerName": "build-container", #may need to replace this
                                    "BlobPrefix": "",
                                    "EnvironmentName": "",
                                    "EnvironmentNameRM": "",
                                    "ResourceFilteringMethod": "machineNames",
                                    "MachineNames": "",
                                    "vmsAdminUserName": "",
                                    "vmsAdminPassword": "",
                                    "TargetPath": "",
                                    "AdditionalArguments": "",
                                    "enableCopyPrerequisites": "false",
                                    "CopyFilesInParallel": "true",
                                    "CleanTargetBeforeCopy": "false",
                                    "skipCACheck": "true",
                                    "outputStorageUri": "",
                                    "outputStorageContainerSasToken": ""
                                },
                                "taskId": "eb72cb01-a7e5-427b-a8a1-1b31ccac8a43",
                                "version": "1.*",
                                "definitionType": "task",
                                "alwaysRun": False,
                                "continueOnError": False,
                                "overrideInputs": {},
                                "condition": "succeeded()",
                                "environment": {}
                            },
                            {
                                "name": "Set App Settings: ",
                                "refName": "",
                                "enabled": True,
                                "timeoutInMinutes": 0,
                                "inputs": {
                                    "ConnectedServiceName": "b96bc246-5aef-4abd-8a6c-73f5113bacb1", #self.service_endpoint.endpoint.id, #"3765b613-bcbb-433b-9971-09a76371193c",
                                    "WebAppName": self.resource.resource['name'], #"dolk-python-appservice",
                                    "ResourceGroupName": self.resource.resource['name'], #"dolk-python-appservice",
                                    "Slot": "",
                                    "AppSettings": "WEBSITE_RUN_FROM_PACKAGE='https://" + self.resource.resource['name'] + ".blob.core.windows.net/build-container/build" + str(self.build.build.id) + ".zip'\nkey2='value2'\noliver='godlike'" #https://dolkpythonconsu9f80.blob.core.windows.net/build-container/build2.zip
                                },
                                "taskId": "9d2e4cf0-f3bb-11e6-978b-770d284f4f2d",
                                "version": "2.*",
                                "definitionType": "task",
                                "alwaysRun": False,
                                "continueOnError": False,
                                "overrideInputs": {},
                                "condition": "succeeded()",
                                "environment": {}
                            }
                        ],
                        "phaseInputs": {
                            "phaseinput_artifactdownloadinput": {
                                "artifactsDownloadInput": {
                                    "downloadInputs": [
                                        {
                                            "artifactItems": [],
                                            "alias": self.build.name,
                                            "artifactType": "Build",
                                            "artifactDownloadMode": "All"
                                        }
                                    ]
                                },
                                "skipArtifactsDownload": False
                            }
                        }
                    }
                ]

        release_definition_environment = models.release_definition_environment.ReleaseDefinitionEnvironment(
            name ="deploy build",
            rank=1,
            retention_policy= retention_policy_environment,
            pre_deploy_approvals=pre_release_approvals,
            post_deploy_approvals=post_release_approvals,
            deploy_phases= deploy_phases,
            deploy_step=release_deploy_step
        )


        release_definition = models.release_definition.ReleaseDefinition(
            name = self.build.name + " pipeline",
            environments=[release_definition_environment],
            artifacts=[artifact]
        )

        
        self._release_client.create_release_definition(release_definition, project.id)



    def create_release(self, release_definition_name):
        project = self.get_project_by_name(self._project_name)
        release_definition = self.get_release_definition_by_name(project, release_definition_name)

        release_start_metadata = models.release_start_metadata.ReleaseStartMetadata(
            definition_id=release_definition.id
        )

        self._release_client.create_release(release_start_metadata, project.id)


    def get_project_by_name(self, name):
        for p in self._core_client.get_projects():
            if p.name == name:
                return p
        return None

    def get_release_definition_by_name(self, project, name):
        for p in self._release_client.get_release_definitions(project.id):
            if p.name == name:
                return p
        return None

    def get_build_by_name(self, project, name):
        for p in self._build_client.get_builds(project=project.id):
            if p.name == name:
                return p
        return None

    def get_retention_policy(self):
        return models.environment_retention_policy.EnvironmentRetentionPolicy(
                    days_to_keep=600, releases_to_keep=3, retain_build=True
                )

    def get_artifact(self, build, project, artifact_name):
        artifacts = self._build_client.get_artifacts(build.id, project)
        artifact = None
        for a in artifacts:
            if a.name == artifact_name:
                artifact = a

        definition_reference = {}
        definition_reference["project"] = {"id":project.id,"name":project.name}
        definition_reference["definition"] = {"id":artifact.id,"name":artifact.name}
        definition_reference["defaultVersionType"] = {"id": "latestType", "name": "Latest"}

        return models.artifact.Artifact(
            source_id = artifact.id,
            alias = artifact.name,
            type = "Build",
            definition_reference=definition_reference)