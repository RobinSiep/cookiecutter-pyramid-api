import os


from {{cookiecutter.project_slug}} import main
from {{cookiecutter.project_slug}}.lib.factories.root import RootFactory
from {{cookiecutter.project_slug}}.models import init_sqlalchemy


def test_init(app_settings, test_settings):
    try:
        router = main(
            {'__file__': os.path.abspath('test.ini')},
            **app_settings
        )
        assert router.root_factory == RootFactory
    finally:
        init_sqlalchemy(test_settings)
