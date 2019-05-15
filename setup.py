import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sabersql",
    version="1.0.0",
    author="William Stevenson",
    author_email="stevenson.w@husky.neu.edu",
    description="SaberSQL is a tool to scrape baseball data from various sources and import it into a MySQL database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liam923/sabersql",
    download_url="https://github.com/liam923/sabersql/archive/v1.0.0.tar.gz",
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
            'sabersql = sabersql.__main__:main',
        ],
    }
)
