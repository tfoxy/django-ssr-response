# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner >=4.0,<5dev'] if needs_pytest else []


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-ssr-response',
    version='0.1.0',
    author='Tomás Fox',
    author_email='tomas.c.fox@gmail.com',
    description='Django Response using React or Vue server side rendering.',
    license='MIT',
    keywords='django ssr response react vue',
    url='https://github.com/tfoxy/django-ssr-response',
    packages=['django_ssr_response'],
    setup_requires=pytest_runner,
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
)
