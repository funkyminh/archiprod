from distutils.core import setup
from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements/install_requires.txt') as reqs:
    install_requires = reqs.read().split('\n')

with open('requirements/dependency_links.txt') as reqs:
    dependency_links = reqs.read().split('\n')

setup(
    name="Archiprod",
    version="0.1.0",
    description="Archiprod ircam audio/video archives",
    long_description=readme,
    author='Samuel Goldszmidt, Minh Dang',
    author_email='samuel.goldszmidt@ircam.fr, minh.dang@ircam.fr',
    url='http://forge.ircam.fr/p/archiprod',
    packages=find_packages(exclude=('docs', )),
    data_files=[('.', ['manage.py', ])],
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links
)
