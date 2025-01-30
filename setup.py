from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='melodi',
    version='0.1.19',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
        'email-validator'
    ],
    author='Melodi Ltd',
    author_email='info@melodi.fyi',
    description='Helper functions for Melodi',
    keywords='melodi',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
