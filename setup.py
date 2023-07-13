from setuptools import setup, find_packages
#import numpy, sys
import re

# auto-updating version code stolen from RadVel
def get_property(prop, project):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + "/__init__.py").read(),
    )
    return result.group(1)

def get_requires():
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line)
    return reqs

setup(
    name="codeastro_19",
    version=get_property("__version__", "codeastro_19"),
#    packages=find_packages,
    install_requires=get_requires()
)