import re
from distutils.core import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

dev_requirements = []
with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

version = ''
with open('pydest/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='pydest',
    author='jgayfer',
    author_email='gayfer.james@gmail.com',
    version=version,
    license='MIT',
    description='an asynchronous Destiny 2 API wrapper',
    install_requires=requirements,
    extras_require={
      'develop': dev_requirements
    },
    packages=['pydest']
)
