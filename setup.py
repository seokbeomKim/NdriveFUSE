from setuptools import setup
from setuptools.command.install import install
from setuptools import Command
from distutils.sysconfig import get_python_lib
import os
import site


install_requires=[
    'rsa',
    'requests',
    'python-magic',
    'clint',
    'simplejson',
    'fusepy',
    'Ghost.py'
]

class Installer(install):
    def run(self):
        install.run(self)
        print "============== Create binary file ====================="
#        path = os.path.join(get_python_lib(), "NdriveFUSE")
        path = os.path.join(site.getsitepackages()[0], "NdriveForLinux")
        cmd = "echo '#!/bin/bash\n \
        python2 "+ os.path.join(path, "NdriveForLinux.py") + " $@' > /usr/bin/NdriveForLinux"
        os.system(cmd)
        cmd = "echo '#!/bin/bash\n \
        python2 "+ os.path.join(path, "generateConfigFile.py") + "' > /usr/bin/NdriveFUSE_Gen"
        os.system(cmd)
        cmd = "chmod +x /usr/bin/Ndrive*"
        os.system(cmd)
        print "============== Completed ====================="

class Clean(Command):
    description = 'Remove build and trash files'
    user_options = [("all", "a", "the same")]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        cmd = "find . \( -name '*.pyc' -o -name '*.egg-info' -o -name '__pycache__' -o -name 'dist' -o -name 'build' \) -print -exec rm -rf {} \;"
        os.system(cmd)

setup(
    name='NdriveForLinux',
    packages=['NdriveForLinux', 'NdriveForLinux/modules', 'NdriveForLinux/ndrive'],
    version='0.0.2',
    description='NAVER Ndrive client for Linux',
    license='GPL v2.0 License',
    author='Sukbeom Kim',
    author_email='sukbeom.kim@gmail.com',
    url='https://github.com/seokbeomKim/NdriveFUSE.git',
    install_requires=install_requires,
    keywords=['NdriveForLinux','ndrive fuse', 'Ndrive FUSE', 'Ndrive client'],
    cmdclass={'install': Installer,
              'clean': Clean}
)
