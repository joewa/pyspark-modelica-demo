import glob
import os
import sys
import shutil
import distutils.cmd
import setuptools
import setuptools.command.build_py
import setuptools.command.build_ext
import pathlib
import pkg_resources
from ModelicaBuildTools import build_script
from ModelicaModels import BouncingBall


suffix = '.so'
SETUP_DIR = pkg_resources.resource_filename(__name__, ".")
omc_lib_path = os.path.join(SETUP_DIR, 'omcsimruntime')


class BuildModelsCommand(distutils.cmd.Command):
  """A custom command to run buildModel on all Modelica models."""

  description = 'run buildModel on all Modelica models'
  user_options = [
      # The format is (long option, short option, description).
      ('modelname', None, 'model name in package ModelicaModels'),
  ]

  def initialize_options(self):
    """Set default values for options."""
    # Each user option must be listed here with their default value.
    self.model_exefile = ''

  def finalize_options(self):
    """Post-process options."""
    if self.model_exefile:
      assert os.path.exists(self.model_exefile), (
          'Model executable file %s does not exist.' % self.model_exefile)

  def run(self):
    """Run command."""
    build_script(BouncingBall)
    # self.model_exefile = mod.xmlFile
    #command = ['/usr/bin/pylint']
    #if self.model_exefile:
    #  command.append('--rcfile=%s' % self.model_exefile)
    #command.append(os.getcwd())
    #self.announce(
    #    'Running command: %s' % str(command),
    #    level=distutils.log.INFO)
    #subprocess.check_call(command)

 
class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command: Build all models when calling pyton setup.py build"""
  def run(self):
    self.run_command('buildmodels')
    setuptools.command.build_py.build_py.run(self)


setuptools.setup(
    name='pymodelicademo',
    version='0.0.1',
    description='Running Modelica models as a Python package',
    author='Joerg Wangemann',
    author_email='joerg.wangemann@gmail.com',
    url='https://github.com/joewa',
    cmdclass={
        'buildmodels': BuildModelsCommand,
        'build_py': BuildPyCommand,
        #'build_ext': CustomExtBuilder,
        #'build_ext': my_build_ext,
    },
    packages=setuptools.find_packages(include=[
        'OMPython', 'DyMat', 'DyMat.Export',  # 'omcsimruntime',
        'ModelicaModels', 'ModelicaModels.*',
    ]),
    include_package_data=True,  # Takes what is defined in MANIFEST.in
    package_data={
        'ModelicaModels': ['ModelicaModels/build/*/*'],
    },
    data_files=[(os.path.join(sys.prefix, 'lib'), glob.glob('omcsimruntime/*'))],

    install_requires=[
        'psutil',
        'future',
        'pandas>=0.23',
        'numpy>=1.17'
    ],
    #extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter']},
    # setup_requires=['psutil'],  # 'omcompiler>=1.18' (nicht gefunden) 'pytest-runner', 'flake8', 
    # tests_require=['pytest'],
    #entry_points={
    #    'console_scripts': ['my-command=exampleproject.example:main']
    #},
    #package_data={'exampleproject': ['data/schema.json']}
)
