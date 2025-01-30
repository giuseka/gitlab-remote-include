# Copyright [2025] Sergio Tonani
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from gitlab import Gitlab


class GilabProjectImporter:
    def __init__(self, gitlab_uri: str, gitlab_token: str, timeout: int = 5, ssl_verify: bool = True):
        self._base_path = f'source/_'
        self._token = gitlab_token
        self._uri = gitlab_uri
        gl_auth = {
            'http_username': None,
            'http_password': None,
            'private_token': gitlab_token,
            'ssl_verify': ssl_verify,
            'timeout': timeout
        }
        self._gitlab_projects = []

        # create client
        self._client = Gitlab(url=self._uri, **gl_auth)
        self._client.auth()

    def add_project(self, alias: str, project_id: str, project_branch: str = 'master',
                    project_path: str = 'docs', replace_from: str = ''):
        self._gitlab_projects.append({
            'alias': alias,
            'id': project_id,
            'branch': project_branch,
            'path': project_path,
            'replace_from': replace_from
        })

    def _download_gitlab_file(self, download_path, gitlab_project, path='docs', branch='master',
                              replace_from='./', replace_to='./'):
        items = gitlab_project.repository_tree(path=path, ref=branch, get_all=True)
        for item in items:
            # create local folder
            if item['type'] == 'tree':
                folder_name = item['path']
                folder_local_name = f'{self._base_path}/{download_path}/{folder_name}'
                if not os.path.exists(folder_local_name):
                    os.makedirs(folder_local_name)
                self._download_gitlab_file(
                    download_path,
                    gitlab_project,
                    path=folder_name,
                    branch=branch,
                    replace_from=replace_from,
                    replace_to=replace_to
                )

            # create local file
            elif item['type'] == 'blob':
                file_name = item['path']
                file_local_name = f'{self._base_path}/{download_path}/{file_name}'
                if not os.path.exists(file_local_name):
                    with open(file_local_name, 'wb') as f:
                        def action(data):
                            if file_name.find('.rst') > 0:
                                f.write(data.replace(replace_from.encode('utf-8'), ('/'+replace_to+'/').encode('utf-8')))
                            elif file_name.find('.md') > 0:
                                f.write(data.replace(replace_from.encode('utf-8'), ('/'+replace_to).encode('utf-8')))
                            else:
                                f.write(data)

                        gitlab_project.files.raw(file_path=file_name, ref=branch, streamed=True, action=action)
                        # print(f'- download file {file_name} from repo {gitlab_project.name}')

    def run(self):
        for prj in self._gitlab_projects:
            # path_prefix = prj['path_prefix']
            alias = prj['alias']
            # gitlab_project_id = prj['id']
            gitlab_project = self._client.projects.get(prj['id'])
            gitlab_project_path = prj['path']
            # project_name = gitlab_project_id
            project_local_path = f'{self._base_path}/{alias}/docs'
            replace_to = f'{os.getcwd()}/{self._base_path}/{alias}/{gitlab_project_path}'

            if not os.path.exists(project_local_path):
                os.makedirs(project_local_path)
            self._download_gitlab_file(
                alias,
                gitlab_project,
                path=prj['path'],
                branch=prj['branch'],
                replace_from=prj['replace_from'],
                replace_to=replace_to,
            )
            print(f'download project: {prj["id"]}')
