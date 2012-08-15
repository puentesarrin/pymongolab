# -*- coding: utf-8 *-*
import os
import sys
import subprocess
try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
from distutils.cmd import Command

version = "1.0-rc1"


class doc(Command):

    description = "generate documentation"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = "doc/build/%s" % version
        try:
            os.makedirs(path)
        except:
            pass
        status = subprocess.call(["sphinx-build", "-E", "-b", "html",
            "doc", path])
        if status:
            raise RuntimeError("documentation step '%s' failed" % ("html",))
        sys.stdout.write("\nDocumentation step '%s' performed, results here:\n"
            "   %s/\n" % ("html", path))

f = open("README.rst")
try:
    try:
        readme_content = f.read()
    except:
        readme_content = ""
finally:
    f.close()

setup(
    name="pymongolab",
    version=version,
    description="PyMongoLab is a client library for MongoLab REST API.",
    long_description=readme_content,
    author=u"Jorge Puente Sarrín",
    author_email="puentesarrin@gmail.com",
    url="http://pymongolab.puentesarr.in",
    keywords=["mongolab", "pymongolab", "mongolabclient", "mongo", "mongodb"],
    install_requires=["pymongo"],
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database"],
    cmdclass={"doc": doc},
)
