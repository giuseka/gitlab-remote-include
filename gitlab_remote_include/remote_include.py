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
import re


class remoteinclude(nodes.General, nodes.Element):
    pass


class RemoteIncludeDirective(SphinxDirective):
    has_content = True

    def run(self):
        return []


def _read_remote_include(app, docname, source, re_string='', re_sub_string=''):
    base_source = source.pop()

    re_string = r'%s' % re_string
    re_sub_string = r'%s' % re_sub_string
    remote_includes = re.findall(re_string, base_source)
    new_source = re.sub(re_string, re_sub_string, base_source)
    source.append(new_source)

    # get project config
    gitlabs = app.config.remote_include_gitlabs

    for ri in remote_includes:
        gitlab = gitlabs[ri[3]]
        gitlab_uri = gitlab['uri']
        gitlab_token = gitlab['token']
        alias = ri[5]
        project_id = ri[7]
        project_branch = ri[9]
        project_path = ri[11]
        replace_in = ri[13]
        sgp = GilabProjectImporter(gitlab_uri, gitlab_token)
        sgp.add_project(
            alias,
            project_id,
            project_branch=project_branch,
            project_path=project_path,
            replace_from=replace_in
        )
        sgp.run()


def read_nodes(app, docname, source):
    back = ''
    if not docname.find('_') == 0:
        nn = len(docname.split('/'))-1
        back = ['../'] * nn
        back = ''.join(back)

    # rst
    re_string = [
        '(',
        '.. remoteinclude:: (.*)',
        '*(:gitlab-id: (.*))',
        '*(:alias: (.*))',
        '*(:project-id: (.*))',
        '*(:project-branch: (.*))',
        '*(:project-path: (.*))',
        '*(:replace-in: (.*))'
        ')',
    ]
    re_sub_string = f'.. include:: {back}_/\g<6>/\g<2>'
    _read_remote_include(app, docname, source, '[\s\n]'.join(re_string), re_sub_string)

    # md
    re_string = [
        '(',
        '.. remoteincludemd:: (.*)',
        '*(:gitlab-id: (.*))',
        '*(:alias: (.*))',
        '*(:project-id: (.*))',
        '*(:project-branch: (.*))',
        '*(:project-path: (.*))',
        '*(:replace-in: (.*))'
        ')',
    ]
    re_sub_string = f'.. include:: {back}_/\g<6>/\g<2>\n   :parser: myst_parser.sphinx_'
    _read_remote_include(app, docname, source, '[\s\n]'.join(re_string), re_sub_string)


def process_nodes(app, doctree, fromdocname):
    pass


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_config_value('remote_include_gitlabs', {}, 'env')

    app.add_node(remoteinclude)
    app.add_directive('remoteinclude', RemoteIncludeDirective)
    app.add_directive('remoteincludemd', RemoteIncludeDirective)
    app.connect('source-read', read_nodes)
    app.connect('doctree-resolved', process_nodes)

    return {
        'version': '0.1',
        'env_version': 1,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
