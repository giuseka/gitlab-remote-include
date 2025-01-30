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

from setuptools import setup


def load_requires():
    with open('requirements.txt') as f:
        requires = f.read()
    return requires


def load_version():
    with open('./gitlab_remote_include/VERSION') as f:
        _version = f.read()
    return _version


version = load_version()

setup(
    name='gitlab_remote_include',
    version=version,
    description='Sphinx plugin - Gitlab remote include',
    long_description=open('README.rst').read(),
    license='Apache v2',
    url='',
    author='Sergio Tonani',
    author_email='sergio.tonani@gmail.com',
    classifiers=[
        f'Development Status :: {version}',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache v2',
        'Programming Language :: Python :: 3.12'
    ],
    keywords='sphinx, gitlab',
    python_requires=">=3.10",
    scripts=[],
    include_package_data=True,
    install_requires=load_requires(),
    dependency_links=[],
    zip_safe=True,
    obsoletes=[],
    entry_points={}
)
