from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-n8n",
    version="1.0.0",
    description="CLI harness for n8n workflow automation — CLI-Anything pattern",
    long_description=open("cli_anything/n8n/README.md").read(),
    long_description_content_type="text/markdown",
    author="Webcomunica Solutions",
    author_email="info@webcomunica.com",
    url="https://github.com/webcomunicasolutions/cli-anything-n8n",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-n8n=cli_anything.n8n.n8n_cli:main",
        ],
    },
    package_data={
        "cli_anything.n8n": ["skills/*.md", "README.md"],
    },
    include_package_data=True,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
)
