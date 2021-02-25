import setuptools

setuptools.setup(
    name="zli",
    version="0.0.3",
    author="Joe",
    author_email="xhd0216@gmail.com",
    description="A small stock package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "urllib3",  
    ],
    entry_points={
        'console_scripts': [
            'download_options = options_codes.download_prices:options_download_main',
        ],
    },
)