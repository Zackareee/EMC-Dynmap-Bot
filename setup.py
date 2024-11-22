from setuptools import setup, find_packages

setup(
    name="emc_dynmap_bot",
    version="0.1.0",
    author="Zackareee",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.12",  # Specify minimum Python version
    install_requires=["numpy", "pandas", "discord.py", "Pillow", "requests", "sqlalchemy"],
    extras_require={
        "dev": ["pytest", "mypy", "black"],  # Additional dependencies for development
    },
    include_package_data=True,  # Includes non-Python files specified in MANIFEST.in
)
