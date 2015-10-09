from setuptools import setup

import mastool

url = 'https://github.com/omaraboumrad/mastool/archive/{}.tar.gz'.format(
    mastool.VERSION)


setup(
    name='mastool',
    packages=['mastool'],
    version=mastool.VERSION,
    description='static analysis for bad or avoidable practices in python',
    author='Omar Abou Mrad',
    author_email='omar.aboumrad@gmail.com',
    url='https://github.com/omaraboumrad/mastool',
    download_url=url,
    keywords=['static', 'analysis', 'practices'],
    classifiers=[],

    entry_points={
        'console_scripts': [
            'mastool = mastool.main:main',
        ]
    }
)
