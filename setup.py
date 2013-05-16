#       -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='connect_four',
    version='1.0',
    description="Connect four app for Django",
    long_description="",
    author='Petr Papousek',
    author_email='ppapousek@gmail.org',
    license='BSD',
    # packages=['connect_four'],
    packages=find_packages(),
    zip_safe=False,
    # install_requires=[
    #     'Django',
    # ],
)
