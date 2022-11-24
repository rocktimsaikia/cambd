from setuptools import find_packages, setup

setup(
    name="cambd",
    version="0.0.1",
    author="Rocktim Saikia",
    author_email="saikia.rocktim@proton.me",
    url="https://github.com/rocktimsaikia/cambd",
    license="MIT",
    description="Cambridge dictionary cli app",
    long_description=open("README.md").read(),
    install_requires=[
        "beautifulsoup4==4.11.1",
        "html5lib==1.1.0",
        "click==8.0.3",
        "halo==0.0.31",
        "requests==2.25.1",
        "rich==12.6.0",
        "simple_term_menu==1.5.2",
    ],
    entry_points={
        "console_scripts": [
            "cambd = cambd.__main__:main",
        ]
    },
    packages=find_packages(),
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
