"""
Publish a new version:

$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags

$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
"""
import codecs
from setuptools import setup


PLUGIN_REGISTRY_VERSION = '0.1'
PLUGIN_REGISTRY_DOWNLOAD_URL = (
    'https://github.com/klattimer/PluginRegistry/tarball/' + PLUGIN_REGISTRY_VERSION
)


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()

setup(
    name='PluginRegistry',
    packages=['PluginRegistry'],
    version=PLUGIN_REGISTRY_VERSION,
    description='Plugin registration module.',
    long_description=read_file('README'),
    license='MIT',
    author='Karl Lattimer',
    author_email='karl@qdh.org.uk',
    url='https://github.com/klattimer/PluginRegistry',
    download_url=PLUGIN_REGISTRY_DOWNLOAD_URL,
    keywords=[
        'plugins'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
)
