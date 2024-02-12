from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='track2p',
    version='0.2.1',
    packages=['track2p'],
    install_requires=[
        'numpy',
        'matplotlib',
        'scikit-image',
        'itk-elastix'],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )