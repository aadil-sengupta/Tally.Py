"""
Setup configuration for Tally Integration Library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tally-integration",
    version="1.0.0",
    author="Aadil Sengupta",
    author_email="aadilsengupta27@gmail.com",
    description="A comprehensive Python library for integrating with Tally accounting software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aadil-sengupta/Tally.Py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    include_package_data=True,
    package_data={
        "tally_integration": ["experimental_tdls/*.tdl"],
    },
    keywords="tally accounting api xml integration erp",
    project_urls={
        "Bug Reports": "https://github.com/aadil-sengupta/Tally.Py/issues",
        "Source": "https://github.com/aadil-sengupta/Tally.Py",
        "Documentation": "https://github.com/aadil-sengupta/Tally.Py/blob/main/README.md",
    },
)
