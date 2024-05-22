from osbot_aws.AWS_Config import AWS_Config
from osbot_aws.apis.ECR import ECR
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

ENV_VARS__REQUIRED = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                      'AWS_ACCOUNT_ID'   , 'AWS_DEFAULT_REGION'   ]

class Nginx_In_Lambda__MVP(Kwargs_To_Self):
    aws_config     : AWS_Config
    container_name : str        = 'nginx_in_lambda__mvp'


    @cache_on_self
    def ecr(self):
        return ECR()

    def ecr_container(self):
        return self.ecr().repositories()
        #return self.container_name