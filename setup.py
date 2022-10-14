import os
import re
import pathlib
from setuptools import setup

regex = "^v(\d+\.\d+\.\d+)$"
TAG = os.getenv("TAG", "v0.0.0")
if not TAG or not re.search(regex, TAG):
    raise ValueError("TAG enviroment variable must be in the format v1.2.3")
version = re.search(regex, TAG).group(1)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="abstra-cli",
    version=version,
    description="Abstra CLI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abstra-app/abstra-cli",
    license="MIT",
    packages=["abstra_cli", "abstra_cli.resources"],
    install_requires=[
        "setuptools",
        "requests",
        "fire",
        "simple_websocket_server",
        "progress",
        "colour",
    ],
    entry_points={
        "console_scripts": [
            "abstra=abstra_cli.cli:main",
            "abstra-cli=abstra_cli.cli:main",
        ],
    },
)
