# Trustle task
# Author: Alex Savatieiev (a.savex@gmail.com)
# Sep 2025

import glob
from os import path

from setuptools import find_packages, setup
from trustyscheduler.const import title, version

workspace = path.abspath(path.dirname(__file__))
README = open(path.join(workspace, 'README.md')).read()

DATA = [
    ('etc', [f for f in glob.glob(path.join('etc', '*'))]),
    ('templates', [f for f in glob.glob(path.join('templates', '*'))]),
]

dependencies = [
    'six>=1.1.0',
    'pyyaml==6.0.2',
    'configparser==7.2.0',
    'requests<=2.32.4'
]

entry_points = {
    "scheduler_server": [
        "trusty_scheduler = deployer.cli_main:entrypoint"
    ]
}


setup(
    name=title,
    version=version,
    author="Alex Savatieiev",
    author_email="a.savex@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10"
    ],
    keywords="scheduler, rest",
    entry_points=entry_points,
    url="",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.conf', '*.env', '*.j2']
    },
    zip_safe=False,
    install_requires=dependencies,
    data_files=DATA,
    license="",
    description="Code created for trustle task specifically",
    long_description=README
)
