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

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from gitlab_remote_include.gilab_project_importer import GilabProjectImporter
from sphinx.util import logging

logger = logging.getLogger(__name__)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_config_value('gitlab_remote_include', {}, 'env')
    gitlabs = app.config.gitlab_remote_include

    for gitlab_id, gitlab_conf in gitlabs.items():
        logger.info(f'Configure gitlab engine: {gitlab_id}')
        gitlab_uri = gitlab_conf['uri']
        gitlab_token = gitlab_conf['token']
        file_types = gitlab_conf['file_types']
        sgp = GilabProjectImporter(gitlab_uri, gitlab_token, file_types=file_types)
        for prj in gitlab_conf['projects']:
            alias = prj['alias']
            project_id = prj['id']
            project_branch = prj['branch']
            script = prj['script'] if 'script' in prj else ''
            env = prj['env'] if 'env' in prj else {}
            exclude = prj['exclude'] if 'exclude' in prj else []
            sgp.add_project(alias, project_id, project_branch=project_branch, exclude=exclude, script=script, env=env)
        sgp.run()

    return {
        'version': '0.1',
        'env_version': 1,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
