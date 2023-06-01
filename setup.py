from setuptools import setup, find_packages

from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

with open('README.md') as f:
    readme = f.read()

# TODO: Decide which license to use
# with open('LICENSE') as f:
#    license = f.read()

name = 'foodypy'
version = '0.0'
release = '0.0.0'

setup(
    name=name,
    version=version,
    description='Food nutrition library with array operations',
    long_description=readme,
    author='Kurt Mohler',
    author_email='kurtamohler@gmail.com',
    url='https://github.com/kurtamohler/foodypy',
    # license=license,
    packages=['foodypy'],
    cmdclass=cmdclass,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc/source')
        }
    },
)
