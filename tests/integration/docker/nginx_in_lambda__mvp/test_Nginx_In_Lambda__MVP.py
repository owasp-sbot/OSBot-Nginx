from os import getenv
from unittest import TestCase

from osbot_aws.aws.boto3.View_Boto3_Rest_Calls import print_boto3_calls
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_name, folder_files, files_names, files_list, file_exists
from osbot_utils.utils.Misc import list_set

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__MVP import Nginx_In_Lambda__MVP, ENV_VARS__REQUIRED, \
    FOLDER__NGINX_IN_LAMBDA__MVP__SOURCE_FILES


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

    def test_files_in_source_files(self):
        expected_files = ['Dockerfile', 'build-and-publish-docker-image.sh', 'index.html', 'nginx.conf']
        files          = self.nginx_in_lambda.files_in_source_files()

        assert list_set(files) == expected_files
        for file_path in files.values():
            assert file_exists(file_path)

    def test_path_source_files(self):
        path_source_files = self.nginx_in_lambda.path_source_files()
        files_in_parh     = files_list(path_source_files, pattern='*')
        assert folder_exists(path_source_files)
        assert folder_name  (path_source_files) == FOLDER__NGINX_IN_LAMBDA__MVP__SOURCE_FILES
        assert 'Dockerfile' in files_names(files_list(path_source_files, pattern='*'))


    def test_setup(self):
        with self.nginx_in_lambda as _:
            setup_data       = _.setup()
            target_repo_info = setup_data.get('target_repo_info')
            assert list_set(setup_data) == ['target_repo_info']
            assert target_repo_info.get('repositoryName') == _.container_name

            assert target_repo_info.get('repositoryArn' ) == _.ecr_container_arn()
