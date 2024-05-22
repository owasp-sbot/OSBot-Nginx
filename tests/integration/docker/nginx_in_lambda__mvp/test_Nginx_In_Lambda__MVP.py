from os import getenv
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__MVP import Nginx_In_Lambda__MVP, ENV_VARS__REQUIRED


class test_Nginx_In_Lambda__MVP(TestCase):
    nginx_in_lambda : Nginx_In_Lambda__MVP

    @classmethod
    def setUpClass(cls):
        cls.nginx_in_lambda = Nginx_In_Lambda__MVP()

    def test_setup(self):
        assert type(self.nginx_in_lambda) is Nginx_In_Lambda__MVP

    def test_check_env_variables(self):
        for env_var_name in ENV_VARS__REQUIRED:
            assert getenv(env_var_name) is not None , f'Env var was not configured: {env_var_name}'

    def test_ecr_container(self):
        containers = self.nginx_in_lambda.ecr_container()
        assert len(containers) == 1
        assert list_set(containers[0]) == ['createdAt', 'encryptionConfiguration', 'imageScanningConfiguration',
                                           'imageTagMutability', 'registryId', 'repositoryArn', 'repositoryName',
                                           'repositoryUri']

        #result = self.nginx_in_lambda.ecr_container()
        #pprint(result)