from osbot_utils.utils.Dev import pprint

from osbot_aws.AWS_Config                       import AWS_Config
from osbot_aws.deploy.Deploy_Lambda             import Deploy_Lambda
from osbot_nginx.utils.Docker_Util__Nginx import Docker_Util__Nginx
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Nginx_In_Lambda__Deploy_Lambda(Kwargs_To_Self):
    aws_config: AWS_Config
    repository_name: str = 'nginx-in-lambda_mvp'

    @cache_on_self
    def util_deploy_lambda(self):
        account_id         = self.aws_config.account_id()
        region_name        = self.aws_config.region_name()
        docker_util        = Docker_Util__Nginx()
        architecture       = docker_util.docker_architecture()
        repository_tag     = docker_util.container_tag__with_arch_and_version()
        lambda_name        = f'{self.repository_name}__{architecture}'
        image_uri          = f'{account_id}.dkr.ecr.{region_name}.amazonaws.com/{self.repository_name}:{repository_tag}'
        deploy_lambda      = Deploy_Lambda(lambda_name)
        deploy_lambda.set_container_image(image_uri)
        if 'arm64' in repository_tag:                                   # update arch if arm64
            deploy_lambda.lambda_function().architecture = 'arm64'      # default is x86_64 (which is amd64)
        return deploy_lambda

    def deploy_lambda(self):
        util_deploy_lambda = self.util_deploy_lambda()
        #return util_deploy_lambda.lambda_function().create()
        update_result = util_deploy_lambda.package.update()
        if update_result:
            last_update_status = util_deploy_lambda.lambda_function().wait_for_function_update_to_complete(max_attempts=200)
            return last_update_status

    def invoke_lambda(self, path='/', return_logs=False):
        payload = { "rawPath"       : path                          ,
                    "requestContext": {"http": {"method": "GET" }}}
        if return_logs:
            return self.util_deploy_lambda().invoke_return_logs(payload)
        else:
            return self.util_deploy_lambda().invoke(payload).get('body')
