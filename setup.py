import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'Django==1.4.10',
    'django-allauth==0.14.1',
    'django_extensions',
    'django-json-rpc',
    'django-redis-sessions==0.4.0',
    'gevent==1.0',
    'gunicorn==18.0',
    'hiredis',
    'PasteScript',
    'py-bcrypt',
    'pymongo==2.6.3',
    'pytz',
    'redis==2.8.0',
    'South',
    ]

setup(name='dd_auth',
      version='0.1',
      description='dd_auth',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: DFSG approved",
        "License :: OSI Approved :: Artistic License",
        ],
      author='Cuteacute Media OG',
      author_email='ai@datadealer.com',
      license='Artistic Licence 2.0 http://www.perlfoundation.org/attachment/legal/artistic-2_0.txt',
      url='https://datadealer.com',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="dd_auth",
      entry_points = """\
      [paste.app_factory]
      main = dd_auth.wsgi:app
      """,
      )

