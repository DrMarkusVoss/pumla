"""setup procedure"""
from setuptools import setup, find_packages
import os

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    extras_require={"dev": ["mypy==0.910", "pylint==2.10.2"]},
)

curpath = os.path.abspath(os.path.curdir)
print("Path to initialise: " + curpath)
print("Path of pumla installation: " + curpath)
mainpath = curpath + "/"
pumla_macros_fn = curpath + "/test/examples/pumla_macros.puml"
pm_comment = "' THIS IS AN AUTOMATICALLY GENERATED FILE BY pumla init \n"
pm_comment = pm_comment + "' DO NOT CHANGE MANUALLY!\n"
pm_comment = pm_comment + "' TO ADOPT THE PATHS TO YOUR SYSTEM, CALL pumla init AGAIN\n"
pm_comment = pm_comment + "' IN THE FOLDER OF THIS FILE HERE!\n"
pm_include_macros = "!include " + mainpath + "pumla_macros_global.puml\n"
pm_include_tv = "!include " + mainpath + "pumla_tagged_values.puml\n"
with open(pumla_macros_fn, "w") as fil:
    fil.write(pm_comment)
    fil.write(pm_include_macros)
    fil.write(pm_include_tv)
fil.close()