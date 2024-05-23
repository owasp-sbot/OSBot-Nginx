from unittest import TestCase

from osbot_utils.utils.Objects import obj_info

from osbot_utils.utils.Dev import pprint

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Cloud_Front import Nginx_In_Lambda__Cloud_Front


class test_Nginx_In_Lambda__Cloud_Front(TestCase):
    nginx_cloud_front: Nginx_In_Lambda__Cloud_Front

    @classmethod
    def setUpClass(cls):
        cls.nginx_cloud_front = Nginx_In_Lambda__Cloud_Front()

    def test_client(self):
        with self.nginx_cloud_front.cloud_front as _:
            assert _.client().meta.service_model.service_id == 'CloudFront'

    def test_distributions(self):
        with self.nginx_cloud_front.cloud_front as _:
            distributions = _.distributions()
            assert type(distributions) is list


