from unittest import TestCase

import pytest
from osbot_utils.utils.Files import file_exists, folder_exists, folder_name, files_names, files_list
from osbot_utils.utils.Misc import in_github_action, list_set

from osbot_nginx.docker.nginx_in_lambda__mvp.Nginx_In_Lambda__Create_Image import Nginx_In_Lambda__Create_Image


class test_Nginx_In_Lambda__Create_Image(TestCase):

    create_image: Nginx_In_Lambda__Create_Image

    @classmethod
    def setUpClass(cls):
        cls.create_image = Nginx_In_Lambda__Create_Image()

    # utils
    def test_create_image_ecr(self):
        if in_github_action():
            pytest.skip('This is not working on GH actions')            # todo: (this create is working but not the push) figure out why the push is not working on GH actions, I think it is to do with the way the latest tag (i.e. version is applied)

        with self.create_image as _:
            create_image_ecr = _.create_image_ecr()
            assert create_image_ecr.path_image() == _.path_source_files()
            assert create_image_ecr.image_name   == _.repository_name

    # methods

    def test_build_image_on_local_docker(self):
        expected_image_vars = ['Architecture', 'Author', 'Comment', 'Config', 'Container',
                               'ContainerConfig', 'Created', 'DockerVersion', 'GraphDriver',
                               'Id', 'Metadata', 'Os', 'Parent', 'RepoDigests', 'RepoTags',
                               'RootFS', 'Size']
        with self.create_image as _:
            result = _.build_image_on_local_docker()
            image  = result.get('image')
            config = image.get('Config')
            assert list_set(result) == ['build_logs', 'image', 'status', 'tags']
            assert result.get('status') == 'ok'
            assert result.get('tags'  ) == [_.ecr_container_uri()]

            if in_github_action():
                assert list_set(image) == expected_image_vars + ['VirtualSize']
                assert image.get('Architecture') == 'amd64'
            else:
                assert list_set(image) == expected_image_vars
                assert image.get('Architecture') == 'arm64'

            assert config == { 'AttachStderr'   : False             ,
                               'AttachStdin'    : False             ,
                               'AttachStdout'   : False             ,
                               'Cmd'            : None              ,
                               'Domainname'     : ''                ,
                               'Entrypoint'     : ['/bin/sh', '-c', '/var/runtime/bootstrap'],
                               'Env'            : [ 'LANG=en_US.UTF-8',
                                                    'TZ=:/etc/localtime',
                                                    'PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin',
                                                    'LD_LIBRARY_PATH=/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib',
                                                    'LAMBDA_TASK_ROOT=/var/task',
                                                    'LAMBDA_RUNTIME_DIR=/var/runtime'],
                               'ExposedPorts'   : {'8080/tcp': {}}  ,
                               'Hostname'       : ''                 ,
                               'Image'          : config.get('Image'),
                               'Labels'         : None               ,
                               'OnBuild'        : None               ,
                               'OpenStdin'      : False              ,
                               'StdinOnce'      : False              ,
                               'Tty'            : False              ,
                               'User'           : ''                 ,
                               'Volumes'        : None               ,
                               'WorkingDir'     : '/var/task'        }

    def test_ecr_push_image(self):
        if in_github_action():
            pytest.skip('This is not working on GH actions')            # todo: figure out why the push is not working on GH actions, I think it is to do with the way the latest tag (i.e. version is applied)
        with self.create_image as _:
            result     = _.ecr_push_image()
            push_image = result.get('push_image')
            assert list_set(result)              == ['ecr_login','push_image']
            assert list_set(push_image)          == ['auth_result', 'push_json_lines']


    def test_ecr_container(self):
        ecr_container = self.create_image.ecr_repository()

        assert list_set(ecr_container) == ['createdAt', 'encryptionConfiguration', 'imageScanningConfiguration',
                                           'imageTagMutability', 'registryId', 'repositoryArn', 'repositoryName',
                                           'repositoryUri']

    def test_files_in_source_files(self):
        expected_files = ['Dockerfile', 'build-and-publish-docker-image.sh', 'index.html', 'nginx.conf']
        files          = self.create_image.files_in_source_files()

        assert list_set(files) == expected_files
        for file_path in files.values():
            assert file_exists(file_path)

    def test_path_source_files(self):
        path_source_files = self.create_image.path_source_files()
        assert folder_exists(path_source_files)
        assert folder_name  (path_source_files) == self.create_image.repository_name
        assert 'Dockerfile' in files_names(files_list(path_source_files, pattern='*'))