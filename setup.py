# -*- coding: utf-8 -*-
"""
    setup

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from setuptools import setup

setup(
    name='Avatax',
    version='0.1dev',
    author='Openlabs Technologies & Consulting (P) Limited',
    author_email='info@openlabs.co.in',
    packages=['avatax', 'avatax.test'],
    license='',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests',
    ],
    test_suite="avatax.test.suite",
    zip_safe=False,
)
