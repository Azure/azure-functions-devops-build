from vsts.vss_connection import VssConnection
import uuid
import datetime
from msrest.serialization import TZ_UTC
from dateutil.relativedelta import relativedelta
import subprocess, json, requests
import vsts.release.v4_1.models as models
from azure_devops_build_manager.pool.pool_manager import PoolManager 

class ReleaseManager(object):

    def __init__(self, base_url='https://{}.visualstudio.com', organization_name="", project_name="", creds=None):
        self._organization_name = organization_name
        self._project_name = project_name
        self._creds = creds
        # set up all the necessary vsts/azure devops sdk requirements
        organization_url = 'https://dev.azure.com/' + self._organization_name
        # Create a connection to the org
        connection = VssConnection(base_url=organization_url, creds=creds)
        # Get a client (the "core" client provides access to projects, teams, etc)
        self._agent_client = connection.get_client("vsts.task_agent.v4_1.task_agent_client.TaskAgentClient")
        self._build_client = connection.get_client('vsts.build.v4_1.build_client.BuildClient')
        self._core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
        self._release_client = connection.get_client('vsts.release.v4_1.release_client.ReleaseClient')

    def create_release_definition(self, build_name, artifact_name, pool_name, release_definition_name):
        pool = self.get_pool_by_name(pool_name)
        project = self.get_project_by_name(self._project_name)
        build = self.get_build_by_name(project, build_name)
        retention_policy_environment = self.get_retention_policy()
        artifact = self.get_artifact(build, project, artifact_name)
        pre_release_approvals, post_release_approvals = self.get_pre_post_approvals()

        release_deploy_step = models.release_definition_deploy_step.ReleaseDefinitionDeployStep(
            id=2
        )

        triggers =  {
            "triggerType": 1,
            "triggerConditions": None,
            "artifactAlias": artifact_name
        }

        deploymentInput = {}
        deploymentInput["parallelExecution"] = { "parallelExecutionType": 0 }
        deploymentInput["queueId"] = pool.id

        blobtask = {}
        blobtask["name"] = "AzureBlob File Copy"
        blobtask_inputs = {}
        blobtask_inputs["SourcePath"] = "drop/build$(Build.BuildId).zip"
        blobtask_inputs["ConnectedServiceNameSelector"] = 'ConnectedServiceNameARM'
        blobtask_inputs["ConnectedServiceNameARM"] = "432ba47c-4d6d-4b23-bda3-463e0c61d853"
        blobtask_inputs["Destination"] = "AzureBlob"
        blobtask_inputs["StorageAccountRM"] = "dolkpythonappse9cae"
        blobtask_inputs["ContainerName"] = 'azure-build'
        blobtask["inputs"] = blobtask_inputs
        blobtask["version"] = "2.*"
        blobtask["definitionType"] = "task"
        blobtask["taskId"] = "eb72cb01-a7e5-427b-a8a1-1b31ccac8a43"

        deploy_phase =  {
                        "deploymentInput": deploymentInput,
                        "rank": 1,
                        "phaseType": 1,
                        "name": "Agent job",
                        "workflowTasks": [blobtask],
                        "phaseInputs": {
                            "phaseinput_artifactdownloadinput": {
                                "artifactsDownloadInput": {
                                    "downloadInputs": [
                                        {
                                            "artifactItems": [],
                                            "alias": artifact_name,
                                            "artifactType": "Build",
                                            "artifactDownloadMode": "All"
                                        }
                                    ]
                                },
                                "skipArtifactsDownload": False
                            }
                        }
                    }
        
        deploy_phases = [deploy_phase]

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
            name = release_definition_name,
            environments=[release_definition_environment],
            artifacts=[artifact],
            triggers=triggers
        )

        
        self._release_client.create_release_definition(release_definition, project.id)

    def list_release_definitions(self):
        project = self.get_project_by_name(self._project_name)
        return self._release_client.get_release_definitions(project.id)

    def create_release(self, release_definition_name):
        project = self.get_project_by_name(self._project_name)
        release_definition = self.get_release_definition_by_name(project, release_definition_name)

        release_start_metadata = models.release_start_metadata.ReleaseStartMetadata(
            definition_id=release_definition.id
        )

        self._release_client.create_release(release_start_metadata, project.id)

    def list_releases(self):
        project = self.get_project_by_name(self._project_name)
        return self._release_client.get_releases(project.id)


    def get_pool_by_name(self, pool_name):
        pool_manager = PoolManager(organization_name=self._organization_name, project_name=self._project_name, creds=self._creds)
        pools = pool_manager.get_pools()
        for pool in pools.value:
            if pool.name == pool_name:
                return pool
        return None


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
        builds = []
        for p in self._build_client.get_builds(project=project.id):
            if p.definition.name == name:
                builds.append(p)
        sorted_builds = sorted(builds, key=lambda x : x.finish_time, reverse=True)
        return sorted_builds[0]

    def get_retention_policy(self):
        return models.environment_retention_policy.EnvironmentRetentionPolicy(
                    days_to_keep=300, releases_to_keep=3, retain_build=True
                )

    def get_artifact(self, build, project, artifact_name):
        artifacts = self._build_client.get_artifacts(build.id, project.id)
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

    def get_pre_post_approvals(self):
        pre_approval = models.release_definition_approval_step.ReleaseDefinitionApprovalStep(
            id = 0,
            rank = 1,
            is_automated = True,
            is_notification_on = False
        )

        post_approval = models.release_definition_approval_step.ReleaseDefinitionApprovalStep(
            id = 0,
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

        return pre_release_approvals, post_release_approvals