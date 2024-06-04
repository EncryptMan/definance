from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='definance',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)