from setuptools import setup, find_packages

setup(
    name = 'framefeed',
    version = '0.1a',
    packages = ['framefeed', ],
    include_package_data = True,
    package_data = { '': ['*.html',] },
    install_requires = ['django-imagekit',],
    author = 'Ilya Khamushkin',
    author_email = 'ilya@khamushkin.com',
    description = 'Simple django photoblog backend',
)
