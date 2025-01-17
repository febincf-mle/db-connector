from setuptools import setup, find_packages


def read_requirements():

    with open("requirements.txt", "r") as file:
        deps = file.readlines()

    return [dep.strip() for dep in deps if not dep.strip().startswith("-e")]


setup(
    name="connect_db",
    version="0.1.0", 
    description="A Python package to connect to various databases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Febin CF",
    author_email="febin.web3dev@gmail.com", 
    license="MIT",
    packages=find_packages(where="connect_db"),
    package_dir={"": "connect_db"},
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)