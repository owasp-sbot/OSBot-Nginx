from os import getenv

from osbot_aws.AWS_Config import AWS_Config

from osbot_aws.aws.route_53.Route_53 import Route_53
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

from osbot_utils.decorators.methods.cache_on_self import cache_on_self

ENV_VAR_NAME__ROUTE_53__HOST_ZONE_ID = "ROUTE_53__HOST_ZONE_ID"

class Nginx_In_Lambda__Create_DNS_Record(Kwargs_To_Self):
    aws_config     : AWS_Config

    @cache_on_self
    def route_53(self):
        return Route_53()

    def hosted_zone_id(self):
        return getenv(ENV_VAR_NAME__ROUTE_53__HOST_ZONE_ID)