from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'setuptools',
    'nose'
]

setup(
    name='discgolfhub',
    version='1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    author='Paul Osborne'
)
