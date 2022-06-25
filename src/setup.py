import os
import shutil
import distutils.cmd
import setuptools
import setuptools.command.build_py
import pkg_resources
#import setuptools.setup
#import setuptools.find_packages
#import setuptools.command.build_py


SETUP_DIR = pkg_resources.resource_filename(__name__, ".")


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
    from ModelicaModels.BouncingBall import buildmodel
    destination_folder = os.path.join(SETUP_DIR, 'ModelicaModels', 'build', "BouncingBall")
    try:
        os.makedirs(destination_folder)
        files2delete = [f for f in os.listdir(destination_folder) if os.path.isfile(f)]
        for f in files2delete:
            os.remove(os.path.join(destination_folder, f))
    except FileExistsError:
        # directory already exists
        pass
    files_before_build = set([f for f in os.listdir(SETUP_DIR) if os.path.isfile(f)])
    mod = buildmodel()
    files_after_build = set([f for f in os.listdir(SETUP_DIR) if os.path.isfile(f)])
    files_new = files_after_build.difference(files_before_build)
    for f in files_new:
        #print(f)
        if not os.path.isfile(os.path.join(destination_folder, f)) :
            shutil.move(f, destination_folder)
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
    },
    packages=setuptools.find_packages(include=['OMPython', 'ModelicaModels', 'ModelicaModels.*']),
    include_package_data=True,  # Takes what is defined in MANIFEST.in
    package_data={'ModelicaModels': ['ModelicaModels/build/*/*',]},
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
