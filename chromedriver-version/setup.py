from setuptools import setup
import os

HERE = os.path.abspath(os.path.dirname(__file__))

requirements = ["requests"]


def read_readme():
    with open(os.path.join(HERE, 'README.md')) as f:
        return f.read()


def get_version():
    with open(os.path.join(HERE, 'VERSION'), 'r') as f:
        return f.read()


setup(
    name="chromedriver-version-resource",
    version=get_version(),
    description='Concourse CI resource for fetching latest chromedriver version',
    long_description=read_readme(),
    url='https://github.com/openstax/concourse-resources/chromedriver-version',
    author='OpenStax Content Engineering',
    license='AGPLv3.0',
    packages=['tests', 'src'],
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'pytest-vcr',
            'pytest-cov',
            'flake8'
        ]
    },
    tests_require=['pytest', 'pytest-vcr'],
    test_suite='tests',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'check = src.check:main',
            'in = src.in_:main',
            'out = src.out:main',
        ]
    }
)
