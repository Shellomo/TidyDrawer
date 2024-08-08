# File: setup.py

from setuptools import setup, find_packages

setup(
    name="tidydrawer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        # Add other dependencies here
    ],
)