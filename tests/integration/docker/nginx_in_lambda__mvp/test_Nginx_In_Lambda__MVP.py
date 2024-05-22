from os import getenv
from unittest import TestCase

from osbot_aws.aws.boto3.View_Boto3_Rest_Calls import print_boto3_calls
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__MVP import Nginx_In_Lambda__MVP, ENV_VARS__REQUIRED


class test_Nginx_In_Lambda__MVP(TestCase):
    nginx_in_lambda : Nginx_In_Lambda__MVP

    @classmethod
    def setUpClass(cls):
        cls.nginx_in_lambda = Nginx_In_Lambda__MVP()

    def test_check_env_variables(self):
        for env_var_name in ENV_VARS__REQUIRED:
            assert getenv(env_var_name) is not None , f'Env var was not configured: {env_var_name}'

    def test_ecr_container(self):
        ecr_container = self.nginx_in_lambda.ecr_container()

        assert list_set(ecr_container) == ['createdAt', 'encryptionConfiguration', 'imageScanningConfiguration',
                                           'imageTagMutability', 'registryId', 'repositoryArn', 'repositoryName',
                                           'repositoryUri']

    def test_setup(self):
        with self.nginx_in_lambda as _:
            setup_data       = _.setup()
            target_repo_info = setup_data.get('target_repo_info')
            assert list_set(setup_data) == ['target_repo_info']
            assert target_repo_info.get('repositoryName') == _.container_name

            assert target_repo_info.get('repositoryArn' ) == _.ecr_container_arn()
