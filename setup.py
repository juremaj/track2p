from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='track2p',
    version='0.5.2',
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'matplotlib==3.5.3',
        'scikit-image==0.20.0',
        'itk==5.4rc2',
        'PyQt5==5.15.10',
        'qtpy==2.4.1',
        'tqdm==4.66.2',
        'scikit-learn==1.4.0',
        'openTSNE==1.0.1',
        'pandas==1.5.3',
        ],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )