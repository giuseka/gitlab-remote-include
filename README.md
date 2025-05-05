# Sphinx plugin - gitlab remote include

git-remote-include is a sphinx plugin used to include **rst** file and **md** saved in external giltab projects in the 
documentation pages.

## Install

### Testing The module
To test the module, you can make a new virtualenv and then install your package:

```console
python3 -m venv test-sphinx
. test-sphinx/bin/activate
python -m pip install --no-cache git+https://github.com/giuseka/gitlab-remote-include.git
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
gitlab_remote_include = {
    'gitlabcloud': {
        'uri': 'https://gitlab.local.com',
        'token': '...',
        'projects': [
            {'id': 147, 'branch': 'master', 'alias': 'observability-platform'}
        ]
    }
}
```

## Links
