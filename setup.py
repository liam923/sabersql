import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sabersql",
    version="0.0.1",
    author="William Stevenson",
    author_email="liam923@verizon.net",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liam923/sabersql",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'sabersql = sabersql.__main__:run',
        ],
    }
)