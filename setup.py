"""
Setup script for PreEII - Pre-enrollment review support software
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="preeii",
    version="2.0.0",
    author="Mauricio Andrés Zamora Hernández",
    author_email="mauricio.zamora@gmail.com",
    description="Pre-enrollment review support software for Industrial Engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mauricio-zamora-ucr/preeii2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "preeii=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
