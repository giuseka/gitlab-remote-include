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
from sphinx.util import logging
import gevent

logger = logging.getLogger(__name__)


class GilabProjectImporter:
    VALID_FILE_TYPE = ['rst', 'md', 'png', 'jpg', 'jpeg', 'svg', 'drawio']

    def __init__(self, gitlab_uri: str, gitlab_token: str, timeout: int = 5, ssl_verify: bool = True):
        self._base_path = f'source/_remote'
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
            #'path': project_path,
            #'replace_from': replace_from
        })

    def _download_gitlab_item(self, item, download_path, gitlab_project, branch):
        # create local folder
        if item['type'] == 'tree':
            folder_name = item['path']
            folder_local_name = f'{self._base_path}/{download_path}/{folder_name}'
            if not os.path.exists(folder_local_name):
                os.makedirs(folder_local_name)
            self._download_gitlab_tree(download_path, gitlab_project, path=folder_name, branch=branch)

        # create local file
        elif item['type'] == 'blob':
            file_name = item['path']
            if file_name.split('.')[-1] not in self.VALID_FILE_TYPE:
                return
            file_local_name = f'{self._base_path}/{download_path}/{file_name}'
            if not os.path.exists(file_local_name):
                with open(file_local_name, 'wb') as f:
                    gitlab_project.files.raw(file_path=file_name, ref=branch, streamed=True, action=f.write)

        logger.info(f'...Write item {item["path"]}')

    def _download_gitlab_tree(self, download_path, gitlab_project, path='/', branch='master'):
        items = gitlab_project.repository_tree(path=path, ref=branch, get_all=True)

        #for item in items:
        jobs = [gevent.spawn(self._download_gitlab_item, item, download_path, gitlab_project, branch)
                             for item in items]
        _ = gevent.joinall(jobs, timeout=60)

    def run(self):
        for prj in self._gitlab_projects:
            alias = prj['alias']
            gitlab_project = self._client.projects.get(prj['id'])
            try:
                self._download_gitlab_tree(alias, gitlab_project, branch=prj['branch'])
                logger.info(f'Download gitlab project {prj["id"]} branch {prj["branch"]} in folder {prj["alias"]}')
            except Exception as e:
                logger.warning(f'Download gitlab project {prj["id"]} branch {prj["branch"]} error: {e}')

