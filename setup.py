from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='track2p',
    version='0.3.3',
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'matplotlib==3.5.3',
        'scikit-image==0.20.0',
        'itk-elastix==0.19.0',
        'PyQt5==5.15.10',
        'qtpy==2.4.1',
        ],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )