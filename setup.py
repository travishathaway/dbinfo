import os
from setuptools import setup

version = '0.1'

description = "Command line tool for running usage \
    statistic reports on MySQL or PostgreSQL"
cur_dir = os.path.dirname(__file__)

try:
    long_description = open(os.path.join(cur_dir, 'README.rst')).read()
except:
    long_description = description


setup(
    name="dbinfo",
    version=version,
    url='http://github.com/travishathaway',
    license='BSD',
    description=description,
    long_description=long_description,
    author='Travis Hathaway',
    author_email='travis.j.hathaway@gmail.com',
    packages=['dbinfo', ],
    install_requires=['setuptools', 'pymysql', 'psycopg2', 'docopt'],
    entry_points="""
[console_scripts]
dbinfo = dbinfo.main:main
""",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Bug Tracking',
    ],
    test_suite='nose.collector',
)
