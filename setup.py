"""setup procedure"""
import os

from setuptools import setup, find_packages
from pumla.main import createPumlaMacrosFile

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    extras_require={"dev": ["mypy==0.910", "pylint==2.10.2"]},
)

print("pumla setup: initialising the examples")
os.chdir("./test/examples")
os.system("pumla init")
print("pumla setup done.")