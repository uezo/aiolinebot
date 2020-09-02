from setuptools import setup, find_packages
from aiolinebot import __version__

setup(
    name="aiolinebot",
    version=__version__,
    url="https://github.com/uezo/aio-linebot-api",
    author="uezo",
    author_email="uezo@uezo.net",
    maintainer="uezo",
    maintainer_email="uezo@uezo.net",
    description="AioLineBotApi provides asynchronous interface for LINE messaging API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples*"]),
    install_requires=["line-bot-sdk", "aiohttp"],
    license="Apache v2",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
