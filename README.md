# ansible-openwisp-wifi-login-pages

Ansible role to deploy and manage [openwisp-wifi-login-pages](https://github.com/openwisp/openwisp-wifi-login-pages).

Required variables:

- ``wifi_login_pages_domains``: a list with the hostname where the app will be reachable.

## Deploying custom static content

Custom static content (HTML files, PDF, etc.) can be deployed
to ``{{ wifi_login_pages_path }}/static/``.

## Deploy organizations configurations and assets

For deploying organization YAML config files and their related static assets (logo, CSS, etc),
it is mandatory to paste the `organizations` directory with all the configuration and assets of
the organizations inside `files/` directory. These files will be uploaded to remote during the
building and deployment of OpenWISP WiFi Login Pages.
