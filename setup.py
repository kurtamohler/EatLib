from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

# TODO: Decide which license to use
# with open('LICENSE') as f:
#    license = f.read()

name = 'eatlib'
version = '0.0'
release = '0.0.0'

setup(
    name=name,
    version=version,
    description='Food nutrition library with array operations',
    long_description=readme,
    author='Kurt Mohler',
    author_email='kurtamohler@gmail.com',
    url='https://github.com/kurtamohler/eatlib',
    # license=license,
    packages=['eatlib'],
)
