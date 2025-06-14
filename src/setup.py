import glob
import os
import subprocess
import sys
import distutils.cmd
import setuptools
import setuptools.command.build_py
import setuptools.command.build_ext
import pkg_resources
from ModelicaBuildTools import build_script
from MM import BouncingBall
from MM import EDrives


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
        if os.path.join(sys.prefix, 'bin') not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + os.path.join(sys.prefix, 'bin')
        r = str(build_script(BouncingBall, "BouncingBall"))
        r += str(build_script(EDrives, "EDrives.Examples.DCDC.DC_Drive_Switching"))
        r += str(build_script(EDrives, "EDrives.Examples.DCDC.DC_Drive_Continuous"))
        r += str(subprocess.run("env | grep PATH", shell=True, capture_output=True, text=True))

        if 'Error' in r:
            raise ValueError('omc stdout:' + str(r))

        # raise ValueError('Raising omc stdout:' + str(r))



class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command: Build all models when calling pyton setup.py build"""
    def run(self):
        self.run_command('buildmodels')
        setuptools.command.build_py.build_py.run(self)


setuptools.setup(
    name='pymodelicademo',
    version='0.0.2',
    description='Running Modelica models as a Python package',
    author='Joerg Wangemann',
    author_email='joerg.wangemann@gmail.com',
    url='https://github.com/joewa',
    cmdclass={
        'buildmodels': BuildModelsCommand,
        'build_py': BuildPyCommand,
    },
    packages=setuptools.find_packages(include=[
        'OMPython', 'DyMat', 'DyMat.Export',
        'ModelicaRuntimeTools', 'MM', 'MM.*',
    ]),
    include_package_data=True,
    package_data={
        'MM': ['build/*'],
    },
    data_files=[(os.path.join(sys.prefix, 'lib'), glob.glob('omcsimruntime/*'))],

    install_requires=[
        'psutil',
        'future',
        'pandas>=1.5',
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
