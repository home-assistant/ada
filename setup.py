"""Hey Ada!"""
from pathlib import Path
from setuptools import setup


setup(
    name="ada",
    version="0.5",
    license="Apache License 2.0",
    author="The Home Assistant Authors",
    author_email="hello@home-assistant.io",
    url="https://home-assistant.io/",
    description="Hey Ada!",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["voice", "home-assistant", "personal"],
    zip_safe=False,
    platforms="any",
    packages=["ada",],
    include_package_data=True,
)
