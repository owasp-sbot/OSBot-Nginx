from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

from osbot_aws.aws.cloud_front.Cloud_Front import Cloud_Front


class Nginx_In_Lambda__Cloud_Front(Kwargs_To_Self):

    cloud_front : Cloud_Front

