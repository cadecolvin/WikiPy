import re
from setuptools import setup

with open('wikipy.py') as f:
    version_re = r"^__version__\s*=\s*'(.*)'"
    version = re.search(version_re, f.read(), re.M).group(1)


setup(
    name='Wikipy',
    packages=['wikipy'],
    install_requires=['requests'],
    version=version,
    license='GNU',
    description='A lightweight Mediawiki API wrapper',
    author='Cade Colvin',
    author_email='cade.colvin@gmail.com'
    )
