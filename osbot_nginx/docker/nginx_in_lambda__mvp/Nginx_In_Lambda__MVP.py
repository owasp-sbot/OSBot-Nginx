from osbot_aws.AWS_Config                                                   import AWS_Config
from osbot_aws.apis.ECR                                                     import ECR
from osbot_utils.base_classes.Kwargs_To_Self                                import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self
from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Create_Image  import Nginx_In_Lambda__Create_Image

ENV_VARS__REQUIRED = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                      'AWS_ACCOUNT_ID'   , 'AWS_DEFAULT_REGION'   ]


class Nginx_In_Lambda__MVP(Kwargs_To_Self):
    aws_config     : AWS_Config
    repository_name : str        = 'nginx-in-lambda_mvp'

    # utils

    @cache_on_self
    def ecr(self):
        return ECR()


    def util__nginx_create_image(self):
        nginx_create_image = Nginx_In_Lambda__Create_Image(repository_name=self.repository_name)
        return nginx_create_image


    def setup(self):
        target_repo_info = self.ecr().repository_info(self.repository_name)
        if not target_repo_info :
            self.ecr().repository_create(self.repository_name)
            target_repo_info = self.ecr().repository_info(self.repository_name)

        setup_data = dict(target_repo_info=target_repo_info)
        return setup_data
