import setuptools

setuptools.setup(
    name="randomthoughts",
    version="0.0.7",
    author="Joe Awake",
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
        "cufflinks==0.17.3",
        "pandas==1.2.3",
        "urllib3",
    ],
    entry_points={
        'console_scripts': [
            'download_options = options_codes.download_prices:options_download_main',
            'download_stocks = stock_codes.download_prices:stocks_download_main',
        ],
    },
)