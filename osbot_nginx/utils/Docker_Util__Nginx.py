from osbot_docker.apis.API_Docker import API_Docker

from osbot_nginx.utils.Version import Version


class Docker_Util__Nginx:

    def docker_architecture(self):
        return API_Docker().client_docker_version_raw().get('Arch')

    def container_tag__with_arch_and_version(self):
        architecture = self.docker_architecture()
        repo_version = Version().value()
        return f'{architecture}_{repo_version}'