"""
Setup file for swdata
"""

from setuptools import setup, find_packages

setup(
    name='swdata',
    version='0.1.0',
    license='MIT',
    description='SW dataset utilities',
    long_description='',

    author='Tadahiro Matsumoto',
    author_mail='tad@gifu-u.ac.jp',
    url='http://www.mat.info.gifu-u.ac.jp/jspad/',

    packages=['swdata'],

    include_package_data=True
)
