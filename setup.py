# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.6'

setup(
    name='pycan',
    version=__version__,
    url='https://github.com/jusbrasil/pycan',
    author=u'Vicente Carlos de Alencar Jr',
    packages=find_packages(),
    include_package_data=True,
    tests_require=['mock'],
    setup_requires=['nose>=1.0', 'coverage']
)
