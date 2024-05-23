from unittest import TestCase

from osbot_aws.aws.route_53.Route_53__Hosted_Zone import Route_53__Hosted_Zone
from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Create_DNS_Record import \
    Nginx_In_Lambda__Create_DNS_Record


class test_Nginx_In_Lambda__Create_DNS_Record(TestCase):
    create_dns_record : Nginx_In_Lambda__Create_DNS_Record
    hosted_zone       : Route_53__Hosted_Zone

    @classmethod
    def setUpClass(cls):
        cls.create_dns_record = Nginx_In_Lambda__Create_DNS_Record()
        cls.hosted_zone       = cls.create_dns_record.hosted_zone()

    # def test_route_53(self):
    #     with self.create_dns_record as _:
    #
    #         #result = _.route_53().hosted_zones()
    #         result = _.route_53().record_sets(hosted_zone_id = hosted_zone_id)
    #         pprint(result)

    def test_a_records(self):
        with self.hosted_zone as _:
            assert 'nginx-amd64.dev.aws.cyber-boardroom.com.' in _.a_records()

    def test_hosted_zone(self):
        with self.hosted_zone as _:
            assert type(_)            == Route_53__Hosted_Zone
            assert list_set(_.info()) == ['CallerReference', 'Config', 'Id', 'Name', 'ResourceRecordSetCount']

            record_sets = _.record_sets()
            assert len(record_sets) > 0

    def test_hosted_zone_id(self):
        assert self.create_dns_record.hosted_zone_id() is not None