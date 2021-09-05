from setuptools import setup, find_packages

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    extras_require={"dev": ["mypy==0.910", "pylint==2.10.2"]},
)
