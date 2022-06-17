import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='abstra-cli',
    version='0.1.1',
    description='Abstra CLI',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abstra-app/abstra-cli",
    license='MIT',
    packages=['abstra_cli'],
    install_requires=['setuptools', 'requests',
                      'fire', 'simple_websocket_server'],
    entry_points={
        'console_scripts': [
            'abstra-cli=abstra_cli:main',
        ],
    },
)
