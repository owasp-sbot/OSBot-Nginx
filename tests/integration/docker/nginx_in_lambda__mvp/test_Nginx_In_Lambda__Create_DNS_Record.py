from unittest import TestCase

from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Create_DNS_Record import \
    Nginx_In_Lambda__Create_DNS_Record


class test_Nginx_In_Lambda__Create_DNS_Record(TestCase):
    create_dns_record : Nginx_In_Lambda__Create_DNS_Record

    @classmethod
    def setUpClass(cls):
        cls.create_dns_record = Nginx_In_Lambda__Create_DNS_Record()

    # def test_route_53(self):
    #     with self.create_dns_record as _:
    #
    #         #result = _.route_53().hosted_zones()
    #         result = _.route_53().record_sets(hosted_zone_id = hosted_zone_id)
    #         pprint(result)

    def test_hosted_zone_id(self):
        assert self.create_dns_record.hosted_zone_id() is not None
        with self.create_dns_record as _:
            hosted_zones = _.route_53().hosted_zones()
            assert len(hosted_zones) == 1
            assert list_set(hosted_zones[0]) == ['CallerReference', 'Config', 'Id', 'Name', 'ResourceRecordSetCount']