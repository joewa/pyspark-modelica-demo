import os
import sys
import pathlib
import subprocess
import importlib.resources
from OMPython.OMRunner import ModelicaSystemRunner

modelName = "BouncingBall"

# Locate BouncingBall.mo within the current package
package_files = importlib.resources.files(__package__)
fn = str(package_files.joinpath("BouncingBall.mo"))
mosfn = fn + 's'

# Locate the build directory relative to the current package
# (Goes up one level to 'MM', then into 'build')
runpath_global = str(package_files.joinpath("..", "build").resolve())

def create_mos_file():
    with open(mosfn, 'w') as mos_file:
        mos_file.write(f'loadFile("{fn}");\n')
        mos_file.write(f'buildModel({modelName});\n')


def run_mos_file():
    # r = os.popen("omc " + mosfn).readlines()
    # return r
    # r = subprocess.run("omc " + mosfn, shell=True, capture_output=True, text=True)
    r = subprocess.run(os.path.join(sys.prefix, 'bin', 'omc') + " " + mosfn, shell=True, capture_output=True, text=True)
    return {'stdout': r.stdout, 'stderr': r.stderr}


def buildmodel(modelName):
    # return ModelicaSystem(fileName=fn, modelName=modelname, useCorba=False)
    # return ModelicaSystem(fileName=fn, modelName="BouncingBall", useCorba=True)
    create_mos_file()
    r = run_mos_file()
    return r


def instantiatemodel(modelName, use_local=True):
    if isinstance(use_local, bool):
        if use_local:
            # Locate build artifacts using importlib
            runpath = str(package_files.joinpath("..", "build").resolve())
        else:
            runpath = str(pathlib.Path(runpath_global).resolve().absolute())
    elif isinstance(use_local, str):
        runpath = str(pathlib.Path(use_local).resolve().absolute())

    mod = ModelicaSystemRunner(
            modelname=modelName,
            runpath=runpath,
        )
    print(f"Runpath: {runpath}")
    return mod
