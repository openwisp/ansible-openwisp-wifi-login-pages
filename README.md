# ansible-openwisp-wifi-login-pages

Ansible role to deploy and manage [openwisp-wifi-login-pages](https://github.com/openwisp/openwisp-wifi-login-pages).

Required variables:

- ``wifi_login_pages_domains``: a list with the hostname where the app will be reachable.

## Deploying custom static content

Custom static content (HTML files, PDF, etc.) can be deployed
to ``{{ wifi_login_pages_path }}/static/``.
