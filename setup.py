from setuptools import setup


setup(
    name = 'mastool',
    packages = ['mastool'],
    version = '0.0.4',
    description = 'static analysis for bad or avoidable practices in python',
    author = 'Omar Abou Mrad',
    author_email = 'omar.aboumrad@gmail.com',
    url = 'https://github.com/omaraboumrad/mastool',
    download_url = 'https://github.com/omaraboumrad/mastool/archive/0.0.4.tar.gz',
    keywords = ['static', 'analysis', 'practices'],
    classifiers = [],

    entry_points={
        'console_scripts': [
            'mastool = mastool.main:main',
        ]
    }
)
