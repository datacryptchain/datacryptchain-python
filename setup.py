from distutils.core import setup

setup(
    name='datacryptchain',
    version='0.0.0.9008',
    packages=['datacryptchain',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    description = "Encryption and Ledger for Research Data",
    readme = "README.txt",
    Homepage = "https://www.datacryptchain.org",
    Issues = "https://www.datacryptchain.org",

    install_requires=[
        "certifi>=2024.2.2",
        "charset-normalizer>=2.0.12",
        "idna>=3.6",
        "Naked>=0.1.32",
        "pkg-resources>=0.0.0",
        "pyasn1>=0.5.1",
        "pycryptodome>=3.20.0",
        "PyYAML>=6.0.1",
        "requests>=2.27.1",
        "rsa>=4.9",
        "shellescape>=3.8.1",
        "urllib3>=1.26.18",
    ],
)



