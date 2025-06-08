from setuptools import setup, find_packages

setup(
    name="pneuracer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "pneuracer=main:main",  # assumes there's a `main()` in main.py
        ]
    },
)
