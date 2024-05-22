from logging import DEBUG, INFO
from os import getenv
from unittest import TestCase

import pytest
from osbot_aws.aws.boto3.View_Boto3_Rest_Calls import print_boto3_calls
from osbot_utils.helpers.html.Html_To_Tag import Html_To_Tag
from osbot_utils.testing.Logging import Logging
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_name, folder_files, files_names, files_list, file_exists
from osbot_utils.utils.Misc import list_set, in_github_action, timestamp_to_str
from osbot_utils.utils.Objects import obj_info

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__MVP import Nginx_In_Lambda__MVP, ENV_VARS__REQUIRED


class test_Nginx_In_Lambda__MVP(TestCase):
    nginx_in_lambda : Nginx_In_Lambda__MVP

    @classmethod
    def setUpClass(cls):
        cls.nginx_in_lambda = Nginx_In_Lambda__MVP()


    def test_setup(self):
        with self.nginx_in_lambda as _:
            setup_data       = _.setup()
            target_repo_info = setup_data.get('target_repo_info')
            assert list_set(setup_data) == ['target_repo_info']
            assert target_repo_info.get('repositoryName') == _.repository_name
            assert target_repo_info.get('repositoryArn' ) == _.util__nginx_create_image().ecr_repository_arn()


    @pytest.mark.skip("run when wanting to test round-trip")  # todo add detection of image hashes so that we run an update
    def test_update_image_and_lambda(self):
        with self.nginx_in_lambda as _:
            nginx_create_image  = _.util__nginx_create_image()
            nginx_deploy_lambda = _.util__nginx_deploy_lambda()
            with Logging(log_to_console=True, log_level=INFO) as logging:
                logging.info(f'in build_image_on_local_docker')
                nginx_create_image.build_image_on_local_docker()
                logging.info(f'in ecr_push_image')
                nginx_create_image.ecr_push_image()
                logging.info(f'in deploy_lambda')
                nginx_deploy_lambda.deploy_lambda()
                logging.info(f'in invoke_lambda')

                raw_html = nginx_deploy_lambda.invoke_lambda()
                with Html_To_Tag(raw_html) as html_tag:
                    assert html_tag.head.title == 'Welcome to nginx!'


    # misc tests (not directly mapped to functions)
    def test___check_env_variables(self):
        for env_var_name in ENV_VARS__REQUIRED:
            assert getenv(env_var_name) is not None , f'Env var was not configured: {env_var_name}'