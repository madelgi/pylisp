try:
    from setuptools import setup
except ImportError:
    from docutils.core import setup

config = {
    'description': 'TODO',
    'author': 'Max Del Giudice',
    'url': 'TODO',
    'author_email': 'maxdelgiudice@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pylisp'],
    'scripts': [],
    'name': 'pylisp'
}

setup(**config)
