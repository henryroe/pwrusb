from distutils.core import setup
from distutils.command.install import install
from distutils.command.build import build
from distutils.sysconfig import get_python_lib
import subprocess
import shutil
import platform
from codecs import open  # To use a consistent encoding
import os
import subprocess
import re

class SetupError(Exception):
    pass

if platform.system() != 'Darwin':
    raise SetupError('pwrusb package is designed for OSX and will not run on other systems.')

if shutil.which('swig') is None:
    raise SetupError('swig must be installed, e.g. with:\n\tbrew install swig')

for cmd in ['g++', 'ld', 'install_name_tool']:
    if shutil.which(cmd) is None:
        raise SetupError(('unable to find {}; probably means you need to install ' + 
                          'Xcode Command Line Utilities').format(cmd))

usb_lib = 'usb-1.0'
strip_whitespace = lambda s: re.sub('[\s+]', '', s)
if (strip_whitespace('ld: library not found for -l{0}'.format(usb_lib)) in 
    strip_whitespace(subprocess.run("ld -l{0}".format(usb_lib), shell=True, 
                                    stderr=subprocess.PIPE).stderr.decode("utf-8"))):
    raise SetupError(("USB library {0} not found, consider installing with, e.g.:\n\t" +
                      "brew install libusb").format(usb_lib))

base_dir = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(base_dir, "__about__.py")) as f:
    exec(f.read(), about)

# Get the long description from the relevant file, converting from md to rst if possible
with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
try:
    from pypandoc import convert
    long_description = convert('README.md', 'rst', format='md')
except (ImportError, OSError) as e:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

class MyBuild(build):
    def run(self):
        subprocess.call("make")
        build.run(self)

print('xyz', get_python_lib())

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      author=about["__author__"],
      author_email=about["__email__"],
      url=about["__uri__"],
      license=about["__license__"],
      cmdclass={'build': MyBuild},
      data_files=[(get_python_lib() + '/', ['_pwrusb_swig_interface.so']),
                  (get_python_lib() + '/', ['libpowerusb.dylib'])],
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Environment :: MacOS X', # only intended for controlling pwrusb strips from Mac OSX
          'Operating System :: MacOS :: MacOS X', 
          
          'Topic :: Home Automation', 
          'Topic :: Scientific/Engineering', 
          
          # How mature is this project? Common values are
          #     Development Status :: 1 - Planning
          #     Development Status :: 2 - Pre-Alpha
          #     Development Status :: 3 - Alpha
          #     Development Status :: 4 - Beta
          #     Development Status :: 5 - Production/Stable
          #     Development Status :: 6 - Mature
          #     Development Status :: 7 - Inactive
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
  #         'Programming Language :: Python :: 2',
  #         'Programming Language :: Python :: 2.6', 
  #         'Programming Language :: Python :: 2.7',
  #         'Programming Language :: Python :: 3',
  #         'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='pwrusb pdu usb power-control',
      py_modules=["pwrusb", "pwrusb_swig_interface"])

