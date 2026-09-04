# Changelog

## Version 1.5.0 [unreleased]

Work in progress.

## Version 1.4.0 [2026-09-04]

### Changes

- Upgraded to WiFi Login Pages 1.3.x (see
  [changelog](https://github.com/openwisp/openwisp-wifi-login-pages/releases/tag/1.3.0)).
- Upgraded Node.js from `20.x` to `24.x`.

### Dependencies

- Updated `ansible-core` compatibility to [`>=2.15,<2.22`](https://github.com/ansible/ansible/releases/tag/v2.21.0).

## Version 1.3.2 [2026-05-12]

### Dependencies

- Bumped `openwisp-utils~=1.2.2`
- Update ansible-core requirement

### Bugfixes

- Updated nodesource and yarn gpg key checksums

## Version 1.3.1 [2025-12-22]

- Default `wifi_login_pages_version` to stable 1.2 branch of openwisp-wifi-login-pages.

## Version 1.3.0 [2025-10-24]

### Features

- Added logrotate config for nginx logs [#46](https://github.com/openwisp/ansible-openwisp-wifi-login-pages/issues/46)

### Changes

- Upgraded to WiFi Login Pages to 1.2.x (see [changelog](https://github.com/openwisp/openwisp-wifi-login-pages/releases/tag/1.2.0))

## 1.2.0 [2024-11-27]

### Changes

- Upgraded to WiFi Login Pages to 1.1.x (see [changelog](https://github.com/openwisp/openwisp-wifi-login-pages/releases/tag/1.1.0))
- Upgraded to Node 20.x

## 1.1.0 [2023-03-01]

- Added dedicated yarn-build tag
- Removed deprecated command args #30
- Run nodejs in prod mode
- Create /var/www/.npm directory

## 1.0.0 [2022-05-04]

First release.
