from osbot_aws.AWS_Config import AWS_Config
from osbot_aws.apis.ECR import ECR
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

ENV_VARS__REQUIRED = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                      'AWS_ACCOUNT_ID'   , 'AWS_DEFAULT_REGION'   ]

class Nginx_In_Lambda__MVP(Kwargs_To_Self):
    aws_config     : AWS_Config
    container_name : str        = 'nginx-in-lambda_mvp'


    @cache_on_self
    def ecr(self):
        return ECR()

    def ecr_container(self):
        return self.ecr().repository_info(self.container_name)

    def ecr_container_arn(self):
        region_name = self.aws_config.region_name()
        account_id  = self.aws_config.account_id()
        return f'arn:aws:ecr:{region_name}:{account_id}:repository/{self.container_name}'

    def setup(self):
        target_repo_info = self.ecr().repository_info(self.container_name)
        if not target_repo_info :
            self.ecr().repository_create(self.container_name)
            target_repo_info = self.ecr().repository_info(self.container_name)

        setup_data = dict(target_repo_info=target_repo_info)
        return setup_data
