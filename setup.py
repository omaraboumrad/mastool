from setuptools import setup

from mastool import extension

url = 'https://github.com/omaraboumrad/mastool/archive/{}.tar.gz'.format(
    extension.__version__)


setup(
    name='mastool',
    packages=['mastool'],
    version=extension.__version__,
    description='static analysis for bad or avoidable practices in python',
    author='Omar Abou Mrad',
    author_email='omar.aboumrad@gmail.com',
    url='https://github.com/omaraboumrad/mastool',
    download_url=url,
    keywords=['static', 'analysis', 'practices'],
    install_requires=[
        'setuptools',
        'flake8',
    ],
    py_modules=['mastool'],

    entry_points={
        'flake8.extension': [
            'mastool = mastool.extension:Mastool',
        ],
    },

    classifiers=[],
)
