from setuptools import setup, find_packages

setup(
    name="Roboarena",
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame>=2.5.1',
        'pygame_gui>=0.6.12',
        'PyTMX>=3.32',
    ],
)
