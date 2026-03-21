from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="datacx",                   
    version="0.1.0",                
    packages=find_packages(),         
    python_requires=">=3.10",        
    include_package_data=True,        
    license="MIT",
    author="Sarvesh",
    description="Python helper module for files JSON and CSV",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)