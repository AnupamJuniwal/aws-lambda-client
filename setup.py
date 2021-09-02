#!/usr/bin/env python
from os import path
from setuptools import setup, find_packages

setup(
    name='aws_lambda_client',
    version='0.1.0',
    description='Lambda client on simple http requests',
    long_description=open('README.md').read(),
    author='AnupamJuniwal',
    url='https://github.com/AnupamJuniwal/aws-lambda-client',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={
        'aws_lambda_client': [
            'data/*.json',
        ]
    },
    include_package_data=True,
    install_requires = [
        'requests'
    ],
    license="GNU General Public License v3.0",
    project_urls={
        'Documentation': 'https://github.com/AnupamJuniwal/aws-lambda-client',
        'Source': 'https://github.com/AnupamJuniwal/aws-lambda-client',
    },
)
