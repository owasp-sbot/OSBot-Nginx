from unittest import TestCase

from osbot_aws.aws.boto3.Capture_Boto3_Error import capture_boto3_error
from osbot_aws.aws.iam.Capture_IAM_Exception import capture_iam_exception
from osbot_nginx.utils.Version import Version
from osbot_utils.decorators.methods.capture_exception import capture_exception
from osbot_utils.helpers.html.Dict_To_Tags import Dict_To_Tags
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Deploy_Lambda import Nginx_In_Lambda__Deploy_Lambda


class test_Nginx_In_Lambda__Deploy_Lambda(TestCase):

    nginx_deploy_lambda: Nginx_In_Lambda__Deploy_Lambda

    @classmethod
    def setUpClass(cls):
        cls.nginx_deploy_lambda = Nginx_In_Lambda__Deploy_Lambda()

    def test_deploy_lambda(self):
        result = self.nginx_deploy_lambda.deploy_lambda()
        assert result == 'Successful'

    def test_invoke_lambda(self):
        raw_html  = self.nginx_deploy_lambda.invoke_lambda()
        assert raw_html is not None
        html_dict = Html_To_Dict(raw_html ).convert()
        html_tags = Dict_To_Tags(html_dict).convert()
        version   = Version().value()
        assert html_tags.head.title == f'Welcome to nginx! {version}'

