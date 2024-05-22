from osbot_aws.AWS_Config                           import AWS_Config
from osbot_aws.apis.ECR                             import ECR
from osbot_aws.helpers.Create_Image_ECR             import Create_Image_ECR
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Files                        import path_combine, files_list, files_recursive, file_name

import osbot_nginx
from osbot_nginx.docker import nginx_in_lambda__mvp

ENV_VARS__REQUIRED = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                      'AWS_ACCOUNT_ID'   , 'AWS_DEFAULT_REGION'   ]

FOLDER__DOCKER__IMAGES_FILES = '../docker_files'

class Nginx_In_Lambda__MVP(Kwargs_To_Self):
    aws_config     : AWS_Config
    repository_name : str        = 'nginx-in-lambda_mvp'

    # utils

    @cache_on_self
    def ecr(self):
        return ECR()

    @cache_on_self
    def create_image_ecr(self):
        return Create_Image_ECR(image_name=self.repository_name, path_images=self.path_docker_image_files())

    # methods

    def build_image_on_local_docker(self):
        return self.create_image_ecr().build_image()


    def ecr_repository(self):
        return self.ecr().repository_info(self.repository_name)

    def ecr_repository_arn(self):
        region_name = self.aws_config.region_name()
        account_id = self.aws_config.account_id()
        return f'arn:aws:ecr:{region_name}:{account_id}:repository/{self.repository_name}'

    def ecr_container_uri(self):
        region_name = self.aws_config.region_name()
        account_id  = self.aws_config.account_id()
        return f"{account_id}.dkr.ecr.{region_name}.amazonaws.com/{self.repository_name}:latest"

    def files_in_source_files(self):
        files = {}
        for file_path in files_recursive(self.path_source_files()):
            files[file_name(file_path)] = file_path
        return files

    def path_source_files(self):
        return path_combine(self.path_docker_image_files(), self.repository_name)

    def path_docker_image_files(self):
        return path_combine(osbot_nginx.path, FOLDER__DOCKER__IMAGES_FILES)

    def setup(self):
        target_repo_info = self.ecr().repository_info(self.repository_name)
        if not target_repo_info :
            self.ecr().repository_create(self.repository_name)
            target_repo_info = self.ecr().repository_info(self.repository_name)

        setup_data = dict(target_repo_info=target_repo_info)
        return setup_data
