# from setuptools import setup
from distutils.core import setup
from distutils.command.install import install
from distutils.command.build import build
from distutils.sysconfig import get_python_lib
import subprocess
import shutil
import pdb

class MyBuild(build):
    def run(self):
        subprocess.call("make")
        build.run(self)

setup(name="pwrusb",
      version="0.2.0",
      description="Control pwrusb.com power strip outlets",
      long_description=open('README.md').read(),
      author='Henry Roe',
      author_email='hroe@hroe.me',
      url='https://github.com/henryroe/pwrusb',
      download_url='https://github.com/henryroe/pwrusb/tarball/0.2.0',
      license="LICENSE.TXT",
      cmdclass={'build': MyBuild},
      data_files=[(get_python_lib() + '/', ['_pwrusb.so']),
                  (get_python_lib() + '/', ['libpowerusb.dylib'])],
      py_modules=["pwrusb"])
