import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION')) as f:
    VERSION = f.read().strip()

requires = [
    'alembic~=1.5.8',
    'apispec[validation]~=4.3.0',
    'bcrypt~=3.2.0',
    'marshmallow~=3.11.1',
    'psycopg2~=2.8.6',
    'pyramid~=1.10.8',
    'pyramid_session_redis~=1.6.0',
    'pyramid_tm~=2.4',
    'sendgrid~=6.6.0',
    'sqlalchemy~=1.3.24',
    'waitress~=1.4.4',
    'zope.sqlalchemy~=1.3'
]

tests_require = [
    'pytest~=6.2.2',
    'pytest-mock~=3.5.1',
    'sqlalchemy_utils~=0.36.8',
    'webtest~=2.0.35'
]

extras = {
    'tests': tests_require
}

setup(
    name='{{cookiecutter.project_slug}}',
    version=VERSION,
    description='{{cookiecutter.project_description}}',
    author="{{cookiecutter.author}}",
    author_email='{{cookiecutter.author_email}}',
    packages=find_packages(),
    tests_require=tests_require,
    install_requires=requires,
    extras_require=extras,
    entry_points="""\
    [paste.app_factory]
    main = {{cookiecutter.project_slug}}:main
    """
)
