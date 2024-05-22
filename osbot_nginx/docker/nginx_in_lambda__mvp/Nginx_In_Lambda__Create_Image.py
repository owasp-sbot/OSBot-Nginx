from osbot_docker.apis.API_Docker import API_Docker

from osbot_aws.apis.ECR import ECR

import osbot_nginx
from osbot_aws.AWS_Config                          import AWS_Config
from osbot_aws.helpers.Create_Image_ECR            import Create_Image_ECR
from osbot_nginx.utils.Docker_Util__Nginx import Docker_Util__Nginx
from osbot_utils.base_classes.Kwargs_To_Self       import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self  import cache_on_self
from osbot_utils.utils.Files                       import path_combine, files_recursive, file_name

FOLDER__DOCKER__IMAGES_FILES = '../docker_files'

class Nginx_In_Lambda__Create_Image(Kwargs_To_Self):

    aws_config      : AWS_Config
    repository_name : str        = 'nginx-in-lambda_mvp'

    @cache_on_self
    def tool__create_image_ecr(self):
        kwargs = dict(image_name  = self.repository_name,
                      image_tag   = self.ecr_repository_tag(),
                      path_images = self.path_docker_image_files())
        return Create_Image_ECR(**kwargs)

    @cache_on_self
    def ecr(self):
        return ECR()

    # methods

    def build_image_on_local_docker(self):
        return self.tool__create_image_ecr().build_image()

    def ecr_repository_tag(self):
        return Docker_Util__Nginx().container_tag__with_arch_and_version()

    def ecr_repository(self):
        return self.ecr().repository_info(self.repository_name)

    def ecr_repository_arn(self):
        region_name = self.aws_config.region_name()
        account_id = self.aws_config.account_id()
        return f'arn:aws:ecr:{region_name}:{account_id}:repository/{self.repository_name}'

    def ecr_container_uri(self):
        region_name = self.aws_config.region_name()
        account_id  = self.aws_config.account_id()
        return f"{account_id}.dkr.ecr.{region_name}.amazonaws.com/{self.repository_name}:{self.ecr_repository_tag()}"


    def ecr_push_image(self):
        ecr_login  = self.tool__create_image_ecr().ecr_login()
        push_image = self.tool__create_image_ecr().push_image()
        return dict(ecr_login=ecr_login, push_image=push_image)

    def files_in_source_files(self):
        files = {}
        for file_path in files_recursive(self.path_source_files()):
            files[file_name(file_path)] = file_path
        return files

    def path_source_files(self):
        return path_combine(self.path_docker_image_files(), self.repository_name)

    def path_docker_image_files(self):
        return path_combine(osbot_nginx.path, FOLDER__DOCKER__IMAGES_FILES)