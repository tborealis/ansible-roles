PHPBU
=====

Database backups. See https://phpbu.de.


Requirements
------------
PHP must already be installed (e.g. via the `php` role) — the role fails fast
if it is not. phpbu is a phar that needs `ext-dom` to parse its XML config, so
include `xml` in `php_extensions`. The role deliberately does not install PHP
itself, since the PHP version and configuration are site-specific.


Updating PHPBU
-------------
See https://phar.phpbu.de/ for releases and checksums.


TODO
----
- Build config from vars rather than templating
