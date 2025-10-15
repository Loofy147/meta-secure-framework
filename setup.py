from setuptools import setup, find_packages

setup(
    name="sacef",
    version="3.1.0",
    author="SACEF Development Team",
    author_email="contact@sacef.dev",
    description="Self-Adversarial Code Evolution Framework (SACEF)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/sacef",  # Replace with the actual URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML>=6.0",
        "z3-solver>=4.12.1.0",
    ],
    entry_points={
        "console_scripts": [
            "sacef=sacef.__main__:main",
        ],
    },
)
