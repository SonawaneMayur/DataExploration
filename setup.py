import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Exploratory_Data_Analysis",
    version="0.0.1",
    author="Mayur Sonawane",
    author_email="mayurs1690@gmail.com",
    description="analyse the parquet file and generate the descriptive stats, character encoding, regression analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SonawaneMayur/Exploratory_Data_Analysis.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
)