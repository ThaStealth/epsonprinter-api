import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epsonprinter",
    version="0.0.7",
    author="ThaStealth",
    author_email="author@example.com",
    description="Communication package for Epson Workforce printer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thastealth/epsonprinter",
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)