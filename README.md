# ansible-openwisp-wifi-login-pages

[![Build Status](https://github.com/openwisp/ansible-openwisp-wifi-login-pages/workflows/Ansible%20OpenWISP%20WiFi%20Login%20Pages%20CI%20Build/badge.svg?branch=master)](https://github.com/openwisp/ansible-openwisp-wifi-login-pages/actions)

Ansible role to deploy and manage [openwisp-wifi-login-pages](https://github.com/openwisp/openwisp-wifi-login-pages).

Required variables:

- `wifi_login_pages_domains`: a list with the hostname where the app will be reachable.
- `wifi_login_pages_organizations_src`: local path of the organization configuration

## Usage (tutorial)

If you don't know how to use ansible, don't panic, this procedure will
guide you towards a fully working basic openwisp-wifi-login-pages installation.

If you already know how to use ansible, you can skip this tutorial.

First of all you need to understand two key concepts:

- for **"production server"** we mean a server (**not a laptop or a desktop computer!**) with public
  ipv4 / ipv6 which is used to host openwisp2
- for **"local machine"** we mean the host from which you launch ansible, eg: your own laptop

Ansible is a configuration management tool that works by entering production servers via SSH,
**so you need to install it and configure it on the machine where you launch the deployment** and
this machine must be able to SSH into the production server.

Ansible will be run on your local machine and from there it will connect to the production server
to install openwisp-wifi-login-pages.

### Install ansible

Install ansible (version 2.10 or higher) **on your local machine** (not the production server!) if
you haven't done already.

To **install ansible** we suggest you follow the official [ansible installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-in-a-virtual-environment-with-pip). It is recommended to install ansible through a virtual environment to avoid dependency issues.

Please ensure that you have the correct version of Jinja installed in your Python environment:
```
pip install Jinja>=2.11
```

### Choose a working directory

Choose a working directory **on your local machine** where to put the configuration of
openwisp-wifi-login-pages.

This will be useful when you will need to upgrade openwisp-wifi-login-pages.

Eg:

```
mkdir ~/openwisp-wifi-login-pages-ansible-playbook
cd ~/openwisp-wifi-login-pages-ansible-playbook
```

Putting this working directory under version control is also a very good idea.

### Install ansible role from ansible-galaxy

```
ansible-galaxy install openwisp.wifi_login_pages
```

### Create inventory file

The inventory file is where group of servers are defined. In our simple case we can
get away with defining just one group in which we will put just one server.

Create a new file called `hosts` **in your local machine**'s working directory
(the directory just created in the previous step), with the following contents:

```
[openwisp-wifi-login-pages]
openwisp-wifi-login-pages.mydomain.com
```

### Create playbook file

Create a new playbook file `playbook.yml` **on your local machine** with the following contents:

```yaml
- hosts: openwisp-wifi-login-pages
  become: "{{ become | default('yes') }}"
  roles:
    - openwisp.wifi_login_pages
  vars:
    wifi_login_pages_domains: ["wifi.openwisp.org"]
```

The line `become: "{{ become | default('yes') }}"` means ansible will use the `sudo`
program to run each command. You may remove this line if you don't need it (eg: if you are
using the `root` user on the production server).

You may replace `openwisp-wifi-login-pages` on the `hosts` field with your production server's
hostname if you desire.

The `wifi_login_pages_domains` is only required vars. It is a list with the hostname where the
app will be reachable.

### Run the playbook

Now is time to **deploy openwisp-wifi-login-pages to the production server**.

Run the playbook **from your local machine** with:

```
ansible-playbook -i hosts playbook.yml -u <user> -k --become -K
```

Substitute `<user>` with your **production server**'s username.

The `-k` argument will need the `sshpass` program.

You can remove `-k`, `--become` and `-K` if your public SSH key is installed on the server.

**Tips**:

- If you have an error like `Authentication or permission failure` then try to use _root_ user
  `ansible-playbook -i hosts playbook.yml -u root -k`
- If you have an error about adding the host's fingerprint to the `known_hosts` file, you can simply
  connect to the host via SSH and answer yes when prompted; then you can run `ansible-playbook` again.

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
docker pull geerlingguy/docker-ubuntu2204-ansible:latest
docker pull geerlingguy/docker-ubuntu2004-ansible:latest
docker pull geerlingguy/docker-debian11-ansible:latest
```

**Step 5**: Install ansible dependencies

```
ansible-galaxy collection install community.docker
```

**Step 6**: Run molecule test

```
molecule test -s local
```

If you don't get any error message it means that the tests ran successfully without errors.

**ProTip:** Use `molecule test --destroy=never` to speed up subsequent test runs.
