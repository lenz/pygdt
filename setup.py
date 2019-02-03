from setuptools import setup, find_packages
from pygdt import VERSION

setup(
    name='pygdt',
    version=VERSION,
    url='https://github.com/lenz/pygdt',
    license='BSD',
    author='Lenz Hirsch',
    author_email='hirsch@seamless.de',
    description='Read and write GDT Files',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['pygdt = pygdt.cli:main'],
    },
    install_requires=[
        'watchdog',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)