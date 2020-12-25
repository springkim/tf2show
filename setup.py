import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tf2show",
    version="0.0.3",
    author="Bomm Kim",
    author_email="aspringnode@gmail.com",
    description="tf2show prints tensorflow2's keras model pretty.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/springkim/tf2show",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'openpyxl>=3.0.0',
    ],
)