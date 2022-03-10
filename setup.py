from setuptools import setup, find_packages

setup(
    name="async-truckersmp",
    version="0.1",
    description="An asynchronous Python API wrapper for TruckersMP.",
    long_description=open("README.rst", "r", encoding="UTF-8").read(),
    url="https://github.com/SamNuttall/Async-TruckersMP",
    author="Sam Nuttall",
    author_email="nuttall.sam@gmail.com",
    license="MIT",
    keywords="truckersmp",
    packages=find_packages(),
    install_requires=open("requirements.txt", "r", encoding="UTF-8").read().strip().splitlines(),
    extra_requires={
        "readthedocs": open("requirements-docs.txt", "r", encoding="UTF-8").read().strip().splitlines()
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
