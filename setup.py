# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pdf2image',

    version='1.5.0',

    description='A wrapper around the pdftoppm and pdftocairo command line tools to convert PDF to a PIL Image list.',

    url='https://github.com/Belval/pdf2image',

    author='Edouard Belval',
    author_email='edouard@belval.org',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='pdf image png jpeg jpg convert',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'pillow',
    ]
)
