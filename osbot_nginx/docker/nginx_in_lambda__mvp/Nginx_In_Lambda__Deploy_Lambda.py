from osbot_aws.AWS_Config                       import AWS_Config
from osbot_aws.deploy.Deploy_Lambda             import Deploy_Lambda
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Nginx_In_Lambda__Deploy_Lambda(Kwargs_To_Self):
    aws_config: AWS_Config
    repository_name: str = 'nginx-in-lambda_mvp'

    @cache_on_self
    def util_deploy_lambda(self):
        account_id         = self.aws_config.account_id()
        region_name        = self.aws_config.region_name()
        image_uri          = f'{account_id}.dkr.ecr.{region_name}.amazonaws.com/{self.repository_name}:latest'
        deploy_lambda      = Deploy_Lambda(self.repository_name)
        deploy_lambda.set_container_image(image_uri)
        deploy_lambda.lambda_function().architecture = 'arm64'
        return deploy_lambda

    def deploy_lambda(self):
        util_deploy_lambda = self.util_deploy_lambda()
        #return util_deploy_lambda.lambda_function().create()
        return util_deploy_lambda.deploy()

    def invoke_lambda(self, path='/', return_logs=False):
        payload = { "rawPath"       : path                          ,
                    "requestContext": {"http": {"method": "GET" }}}
        if return_logs:
            return self.util_deploy_lambda().invoke_return_logs(payload)
        else:
            return self.util_deploy_lambda().invoke(payload).get('body')
