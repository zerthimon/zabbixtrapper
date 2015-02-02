from setuptools import setup

setup(
    name="zabbixtrapper",
    version="0.0.1",
    install_requires=[],
    description="Zabbix Trapper Python interface library",
    author="Lior Goikhburg",
    author_email="goikhburg@gmail.com",
    license="GPL",
    keywords="zabbix trapper library",
    url="https://github.com/zerthimon/python_zabbix_trapper",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    packages=["zabbixtrapper"],
)
