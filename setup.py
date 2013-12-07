from setuptools import setup, find_packages

setup(name='django_openflights',
      packages=find_packages(),
      version=0.1,
      description="Django models and import management commands for OpenFlights.org data",
      author="David Gouldin",
      author_email="david@gould.in",
      url="http://gould.in",
      install_requires=[
      'Django'
      ]
     )
