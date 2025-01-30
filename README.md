# Sphinx plugin - gitlab remote include

git-remote-include is a sphinx plugin used to include **rst** file and **md** saved in external giltab projects in the 
documentation pages.

## Install

### Testing The module
To test the module, you can make a new virtualenv and then install your package:

```console
python3 -m venv test-sphinx
. test-sphinx/bin/activate
python setup.py install

python setup.py build
```

## Getting started

Add the plugin in sphinx conf.py.

```
extensions = [
    ...
    'myst_parser',
    'gitlab_remote_include'
]
```

**myst_parser** is another extension needed if you want to include **md** files.

### Configure the plugin

Add the configuration in conf.py

```
remote_include_token = '<gitlab token>'
remote_include_uri = 'https://gitlab-cloud.cervedgroup.com'
```

## Links
