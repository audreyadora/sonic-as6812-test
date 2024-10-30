from setuptools import setup


setup(
   name='sonic-platform',
   version='1.0',
   description='SONiC platform API implementation on Marvell MVTX9180  Platforms',
   license='Apache 2.0',
   author='SONiC Team',
   author_email='sonic_dbmvtx9180@marvell.com',
   url='',
   maintainer='Marvell MVTX9180',
   maintainer_email='',
   packages=[
       'sonic_platform'
   ],
   package_dir={'sonic_platform': 'dbmvtx9180/sonic_platform'},
   classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
   ],
   keywords='sonic SONiC platform PLATFORM',
)
