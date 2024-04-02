# coding: utf-8

from distutils.core import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='gpttsrt',
    version='0.0.1',
    description='Gpt powered subtitle translation tool.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Seeker472',
    author_email='gmx472@qq.com',
    url='https://github.com/Seeker0472/gpttsrt',
    packages=['gpttsrt'],
    entry_points={
        'console_scripts': [
            'gpttsrt = gpttsrt.gpttsrt:main',
        ],
    },
    install_requires=[
        'pysrt~=1.1.2',
        'requests',
        'tqdm~=4.65.0',
        'configargparse~=1.4',
        'openai~=1.9.0',
    ],
)
