from os import getenv
from unittest import TestCase

import pytest

from osbot_utils.testing.Logging import Logging

from osbot_aws.aws.route_53.Route_53__Hosted_Zone import Route_53__Hosted_Zone
from osbot_utils.utils.Misc import list_set, timestamp_utc_now

from osbot_utils.utils.Dev import pprint

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Create_DNS_Record import \
    Nginx_In_Lambda__Create_DNS_Record

ENV_NAME__ROUTE_53__ROOT_DOMAIN_NAME = 'ROUTE_53__ROOT_DOMAIN_NAME'

@pytest.mark.skip("needs test domains to work")
class test_Nginx_In_Lambda__Create_DNS_Record(TestCase):
    create_dns_record : Nginx_In_Lambda__Create_DNS_Record
    hosted_zone       : Route_53__Hosted_Zone
    root_domain       : str

    @classmethod
    def setUpClass(cls):
        cls.create_dns_record = Nginx_In_Lambda__Create_DNS_Record()
        cls.hosted_zone       = cls.create_dns_record.hosted_zone()
        cls.root_domain       = getenv(ENV_NAME__ROUTE_53__ROOT_DOMAIN_NAME)

    # def test_route_53(self):
    #     with self.create_dns_record as _:
    #
    #         #result = _.route_53().hosted_zones()
    #         result = _.route_53().record_sets(hosted_zone_id = hosted_zone_id)
    #         pprint(result)

    def test_a_records(self):
        with self.hosted_zone as _:
            assert len(_.a_records()) > 0

    # note: at the moment this test doesn't wait for changes to be propagated since they can take quite a while (i.e. a couple minutes)
    @pytest.mark.skip("needs active CF distribution")
    def test_create_a_record(self):
        target_cloud_front    = '...'       # todo: needs live CF distribution
        hosted_zone_id        = '...'
        target_hosted_zone_id = '...'

        #logging = Logging().enable_log_to_console()
        with self.hosted_zone as _:
            record_name = 'test-domain-2.' + self.root_domain
            create_kwargs = dict(record_name            = record_name        ,
                                 alias_target           = target_cloud_front   ,
                                 hosted_zone_id         = hosted_zone_id       ,
                                 alias_hosted_zone_id   = target_hosted_zone_id)

            #logging.info('Step 1: create_new_a_record')
            create_result    = _.create_new_a_record(**create_kwargs)


            #logging.info('Step 2: checking dns answer for dns entry')
            dns_answer = _.check_dns_answer(record_name)
            assert dns_answer.get('RecordName') == record_name

            # assert list_set(dns_answer) == ['Nameserver', 'Protocol', 'RecordData', 'RecordName', 'RecordType', 'ResponseCode']
            # assert dns_answer.get('ResponseCode') == 'NOERROR'

            #logging.info('Step 3: deleting record')
            delete_result = _.delete_record_set__a__to_alias(dns_entry=record_name, alias_dns_name=target_cloud_front, alias_hosted_zone_id=target_hosted_zone_id)
            assert delete_result.get('Status') == 'PENDING'

            #pprint(result)

            # change_id      = '/change/C0469099RF6OOLFFYH8C'
            # change_details = _.route_53.change_details(change_id)
            # assert list_set(change_details) == ['Id', 'Status', 'SubmittedAt']
            # pprint(_.route_53.wait_for_change_status(change_id, 'INSYNC'))

            # timestamp_start = timestamp_utc_now()
            # logging.info(f'Step 2: waiting for new record to be done: {create_change_id}')
            # result = _.route_53.wait_for_change_completed(create_change_id,max_attempts=120)
            #
            # if result:
            #     logging.info('Step 3: change done')
            # else:
            #     logging.info('Step 3: change NOT')
            #
            # timestamp_end = timestamp_utc_now()
            # duration = timestamp_end - timestamp_start
            # logging.info(f'Step 4: DNS changewaited for {duration/1000} seconds')
            # #pprint(result)

#

    def test_hosted_zone(self):
        with self.hosted_zone as _:
            assert type(_)            == Route_53__Hosted_Zone
            assert list_set(_.info()) == ['CallerReference', 'Config', 'Id', 'Name', 'ResourceRecordSetCount']

            record_sets = _.record_sets()
            assert len(record_sets) > 0

    def test_hosted_zone_id(self):
        assert self.create_dns_record.hosted_zone_id() is not None

