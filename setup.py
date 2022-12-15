"""
Setup routine for the factory_modeling python package.

The required packages are placed in the "requirements" folder.
"""
import os

import datetime as dt
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="factory_modeling",
    version=dt.date.today().strftime("%Y.%m.%d"),
    author="gahrb",
    author_email="info@gahrb.dev",
    description="A package for modeling factory operations.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="factory.gahrb.dev",
    packages=find_packages(),
    install_requires=read("requirements/requirements.txt").splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
)

# EOF
