#!/usr/bin/env python

try:
    import setuptools
except ImportError:
    from distutils.core import setup

setuptools.setup(
    name='agenerate',
    description='Cloudformation template generator',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'argparse',
        'troposphere',
    ],
    entry_points={
        'console_scripts': [
            'agenerate = agenerate.main:entry',
        ],
    },
    zip_safe=False,
)