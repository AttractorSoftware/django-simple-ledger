# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
setup(
    name='django-simple-ledger',
    version='0.0.1-dev',
    author=u'Azamat Tokhtaev',
    author_email='krik123@gmail.com',
    url='https://github.com/azamattokhtaev/django-simple-ledger',
    license='BSD License',
    description='Simple ledger application for django that can store transaction between any objects',
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
)
