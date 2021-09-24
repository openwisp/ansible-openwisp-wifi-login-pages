# ansible-openwisp-wifi-login-pages

Ansible role to deploy and manage [openwisp-wifi-login-pages](https://github.com/openwisp/openwisp-wifi-login-pages).

Required variables:

- `wifi_login_pages_domains`: a list with the hostname where the app will be reachable.

## Deploy organizations configurations and assets

For deploying organization YAML config files and their related static assets (logo, CSS, etc), proceed
with the following steps:

**Step 1**: Change directory to ansible playbook file.

```
cd <path_to_playbook_file >
```

**Step 2**: Create the directory `files`.

```
mkdir files
```

**Step 3**: Copy all the organizations configuration and assets from `organizations` directory
to the `files/owlp_organizations`.

```
cp -r <path_to_organizations_directory> files/owlp_organizations
```

## Deploy translations

For deploying normal and custom translations copy all the translations from `i18n` directory to
the `files/owlp_i18n`.

```
cp -r <path_to_i18n_directory> files/owlp_i18n
```

Now run the playbook and the files will be uploaded to remote.

## Deploying custom static content

For deploying custom static content (HTML files, PDF, etc.) add all the static content inside
`files/owlp_static` directory.
The files inside `owlp_static` will be uploaded to remote `static` directory while running
the playbook.

## How to run tests

If you want to contribute to `ansible-openwisp-wifi-login-pages` you should run tests
in your development environment to ensure your changes are not breaking anything.

To do that, proceed with the following steps:

**Step 1**: Clone `ansible-openwisp-wifi-login-pages`

Clone repository by:

```
git clone https://github.com/<your_fork>/ansible-openwisp-wifi-login-pages.git
```

**Step 2**: Install docker

If you haven't installed docker yet, you need to install it (example for linux debian/ubuntu systems):

```
sudo apt-get install docker.io
```

**Step 3**: Install molecule and dependences

```
pip install molecule[docker] yamllint ansible-lint docker
```

**Step 4**: Download docker images

```
docker pull geerlingguy/docker-ubuntu2004-ansible:latest
docker pull geerlingguy/docker-debian11-ansible:latest
```

**Step 5**: Run molecule test

```
molecule test -s local
```

If you don't get any error message it means that the tests ran successfully without errors.

**ProTip:** Use `molecule test --destroy=never` to speed up subsequent test runs.
