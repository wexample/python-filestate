from setuptools import setup, find_packages

setup(
    name='wexample-filestate',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='A tool for managing file states, with configuration files in YAML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-filestate',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pydantic',
        'pyyaml',
        'wexample-helpers',
        'wexample-helpers-yaml',
        'wexample-prompt'
    ],
    python_requires='>=3.6',
)
