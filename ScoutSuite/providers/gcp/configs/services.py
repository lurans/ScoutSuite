# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.cloudsql.service import CloudSQL
from ScoutSuite.providers.gcp.services.cloudstorage import CloudStorageConfig
from ScoutSuite.providers.gcp.services.iam import IAMConfig
from ScoutSuite.providers.gcp.services.stackdriverlogging import StackdriverLoggingConfig
from ScoutSuite.providers.gcp.services.computeengine import ComputeEngineConfig
from ScoutSuite.providers.gcp.services.cloudresourcemanager import CloudResourceManager

try:
    from ScoutSuite.providers.gcp.services.kubernetesengine_private import KubernetesEngineConfig
except ImportError:
    pass


class GCPServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, thread_config=4, projects=None, **kwargs):
        super(GCPServicesConfig, self).__init__(credentials)
        
        projects = [] if projects is None else projects

        gcp_facade = GCPFacade()

        self.cloudresourcemanager = CloudResourceManager(thread_config=thread_config)
        self.cloudstorage = CloudStorageConfig(thread_config=thread_config)
        self.cloudsql = CloudSQL(gcp_facade)
        self.computeengine = ComputeEngineConfig(thread_config=thread_config)
        self.iam = IAMConfig(thread_config=thread_config)

        try:
            self.kubernetesengine = KubernetesEngineConfig(thread_config=thread_config)
        except NameError as _:
            pass

        self.stackdriverlogging = StackdriverLoggingConfig(thread_config=thread_config)
        # self.stackdrivermonitoring = StackdriverMonitoringConfig(thread_config=thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'

    def set_projects(self, projects):
        """
        Set the projects attribute of each of the configs. This is because before authentication (when configs
        are instanciated, the projects within an organization are not known).

        :param projects: List of projects to set
        :return: None
        """

        for c in vars(self):
            setattr(getattr(self, c), 'projects', projects)

