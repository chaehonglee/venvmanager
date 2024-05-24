from setuptools import setup, find_packages

setup(
    name="venvmanager",
    version="0.1",
    packages=find_packages(),
    py_modules=['venvmanager'],
    entry_points={
        'console_scripts': [
            'venvmanager=venvmanager:main',
        ],
    },
    install_requires=[],
)