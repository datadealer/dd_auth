# dd_auth #

A service providing user signin/signup for [Data Dealer](http://datadealer.com)

`dd_auth` uses [Django](https://www.djangoproject.com/) authentication framework 
and [django-allauth](http://www.intenct.nl/projects/django-allauth/) to provide
both local and social authentication for Data Dealer players. 

Session data is written to a Redis database using 
[django-redis-sessions](https://pypi.python.org/pypi/django-redis-sessions) django session backend.
`dd_app` services access the same Redis instance and decode session data for clients, extracting
authentication information. Routines connected to django-allauth signals ensure that some of the
user data kept in `dd_auth` database is synced to user-objects in `dd_app` MongoDB game database.

`dd_auth` also includes template modifications and hooks to allow invitation-only access, if needed.

`dd_invitations` component provides very basic means to create, check and invalidate invitation tokens.

## Setting up a development environment ##

### WARNING

Proceed with caution! `dd_auth` can be only considered as a proof-of-concept. It may contain 
parts in dire need of a cleanup and rests of obsolete concepts and ideas. Some of its concepts 
should be reworked ASAP. There are no testsuites provided.

### Required services

Before you begin, you should setup following services/components. 

* a Redis instance to store session data shared with `dd_app`
* a MongoDB instance for game data
* a Django-ORM compatible relational database storage. For testing purposes, a
sqlite database may suite your needs. Still, we strongly recommend to setup
a PostgreSQL or MySQL database for this purpose.

Take a look at Data Dealer stack documentation (TODO) for examples.

### Install requirements

* python 2.7
* virtualenv
* pip
* libevent including development files
* git

For example, MacPort users should run:

    $ sudo port select python python27
    $ sudo port install libevent
    $ export CFLAGS="-I /opt/local/include"

### Setup a virtual environment ###

Create and activate a virtual environment:

    $ virtualenv --no-site-packages /path/to/venv
    $ source /path/to/venv/bin/activate

### Install requirements ###

Setup the application environment:

    $ python setup.py develop

### Clone `dd_auth` repository

    $ cd /path/to/accomodate/dd_auth/components
    $ git clone https://github.com/datadealer/dd_auth.git
    $ cd dd_auth

### Configure application ###

Create a local configuration file `dd_auth/settings_local.py`

You have to set at least some of the configuration parameters in `dd_auth/settings_local.py`:

* set `SECRET_KEY` to a unique, random string specific to your installation
* set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` to configure your mail relay for notifications.
* set `SERVER_EMAIL` and `DEFAULT_FROM_EMAIL` to configure notification sender address.
* set `SESSION_REDIS_` variables (see `dd_auth/settings.py`) to connect to your Redis instance to store session data.
* set `DD_MONGO_DB` (see `dd_auth/settings.py`) to connect to your MongoDB database.
* set `DATABASES` (see `dd_auth/settings.py`) to configure django db storage backend. Default is a sqlite3 file.
* set `ALLOWED_HOSTS` to a list of strings containing domain names you intend to serve Data Dealer game under, 
for example `['datadealer.local', ]. See [Django documentation](https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts)
* you may want to set `SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` according to you setup.
* if you intend to access `dd_auth` over TLS/SSL using some kind of HTTPS terminator proxying requests to `dd_auth`, 
you may need to provide means for `dd_auth` to detect requests coming over a TLS/SSL encrypted connection, for example
by configuring your HTTPS terminator to inject a specific HTTP header into proxied requests. Tell Django how to detect them
by setting `SECURE_PROXY_SSL_HEADER` configuration variable. For example: `SECURE_PROXY_SSL_HEADER=('HTTP_X_PROTO', 'SSL')`. 
Consult [Django documentation](https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER) for details.
* set `INVITATION_REQUIRED` to `True` if you only wish to allow signups for clients providing an invitation token.
* Depending on you setup, you may want to set `LOGIN_REDIRECT_URL`, `ACCOUNT_LOGOUT_REDIRECT_URL` and `INVITATION_FAILED`
to custom values. 
* set `STATIC_ROOT` to a directory you wish to serve static files to HTTP clients from, if default does not suit your needs.
* depending on social auth provides you intend to use with `dd_auth`, you may need to customize `INSTALLED_APPS` and `django-allauth`
specific settings like `SOCIALACCOUNT_PROVIDERS`. See [django-allauth documentation](http://django-allauth.readthedocs.org/en/latest/)
for details.

Consult [Django documentation](https://docs.djangoproject.com/en/1.4/) for details on Django configuration settings.

## Setup a database adapter

Install a proper database adapter. For example, if you use a PostgreSQL database as `dd_auth` storage backend:

    $ pip install postgresql_psycopg2

### Initialise database ###

    $ ./manage.py syncdb
    $ ./manage.py migrate

### Populate static directory

    $ ./manage.py collectstatic

### compile i18n messages in dd_auth app (dd_auth/dd_auth)

    $ ./dd_auth/django-admin.py compilemessages

### Configure wsgi server ###

Use `dev.ini` as a template:

    $ cp dev.ini local.ini

Edit `local.ini` according to your needs.
You'd probably need to change following values:

* In section `[server:main]` - wsgi server configuration
    * set `host`, `port` and `workers` according to your needs

### Start the application ###

Use paster to start the wsgi workers:

    $ paster serve local.ini

### Use [supervisord](http://supervisord.org/) to control your `dd_auth` workers

supervisord configuration snippet example:

    [program:dd_auth]
    command = /path/to/venv/bin/paster serve local.ini
    process_name = dd_auth
    directory = /path/to/accomodate/dd_auth/components/dd_auth
    user = user_to_run_dd_auth_as
    autostart = true
    autorestart = true
    redirect_stderr = true
    stdout_logfile = /path/to/logfiles/%(program_name)s-out.log
    stdout_logfile_maxbytes = 10MB
    stdout_logfile_backups = 10
    stderr_logfile = /path/to/logfiles/%(program_name)s-err.log
    stderr_logfile_maxbytes = 10MB
    stderr_logfile_backups = 10
    priority = 20
    environment=PYTHON_EGG_CACHE='/homedir/of/user_to_run_dd_auth_as/.%(program_name)s_python_eggs'

Consult [supervisord documentation](http://supervisord.org/) for details

### Access admin interface ###

Admin interface should now be accessible at `http://host:port/dd_auth_admin` with admin credentials as configured earlier.

*warning*
Static files (css, javascript, images) won't be served this way. You have to setup a HTTP server 
(`nginx`, for example) to serve contents of `STATIC_ROOT` under 

    <domain name you use to access your Data Dealer setup>/dd_auth_static/

for example, `https://datadealer.local/dd_auth_static/`.


For testing purposes, you may also try to set the settings variable `DD_SERVE_STATIC` to `True`
in your local settings. This would force django to serve static files. This is untested and not
recommended.

Take a look at Data Dealer stack documentation (TODO) for examples and details on setting up
a HTTP server.

### Setup Django site object, `django-allauth` social auth adapters etc.

For `dd_auth` to be able to provide social authentication against providers configured by default,
you have to setup a proper django Site object and create "social app" descriptor objects for `django_allauth`
for facebook and google social auth providers. See [django-allauth documentation](http://django-allauth.readthedocs.org/en/latest/)
and [other ressources](http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/) for details.

## Copyright

Copyright (c) 2011-2014, Cuteacute Media OG
`dd_auth` is released under the Artistic License 2.0. See `LICENSE.txt`
