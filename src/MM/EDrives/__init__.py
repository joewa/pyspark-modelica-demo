import os
import subprocess
import sys
# import importlib.resources # Changed
from importlib.resources import files
# from OMPython import ModelicaSystem
from OMPython.OMRunner import ModelicaSystemRunner


# modelName = "EDrives.Examples.DCDC.DC_Drive_Switching"
package_files = files(__package__)
fn = str(package_files.joinpath("EDrives", "package.mo"))

def get_mosfn(modelName):
    return str(files(__name__).joinpath(modelName + ".mos"))

runpath_global = str(files(__name__).joinpath("..", "build"))


def create_mos_file(mofile, modelName, mosfn, install_msl=False, load_msl=False):
    mos_file = open(mosfn, 'w', 1)
    if install_msl:
        # TODO: check if already installed
        mos_file.write('installPackage(Modelica, "3.2.3");\n')
        mos_file.write('getErrorString();\n')
    if load_msl:
        omsl_lib_path = os.path.join(sys.prefix, 'lib', 'omlibrary')
        mos_file.write('setModelicaPath("' + omsl_lib_path + '");\n')
        mos_file.write('getErrorString();\n')
        mos_file.write('loadModel(Modelica);\n')
        mos_file.write('getErrorString();\n')
    mos_file.write('loadFile("' + mofile + '");\n')
    mos_file.write('getErrorString();\n')
    # mos_file.write('setComponentModifierValue(CalledbyPython,b,$Code(="+str(newb)+"));\n')
    mos_file.write('buildModel(' + modelName + ');\n')
    mos_file.write('getErrorString();')
    mos_file.close()
    pass


def run_mos_file(mosfn):
    # r = os.popen("omc " + mosfn).readlines()
    # return r
    r = subprocess.run(os.path.join(sys.prefix, 'bin', 'omc') + " " + mosfn, shell=True, capture_output=True, text=True)
    return {'stdout': r.stdout, 'stderr': r.stderr}


def buildmodel(modelName):
    mosfn = get_mosfn(modelName)
    create_mos_file(fn, modelName, mosfn, load_msl=True)
    r = run_mos_file(mosfn)
    return r


def instantiatemodel(modelName, use_local=True):
    if use_local:
        runpath = str(files(__name__).joinpath("..", "build"))
    else:
        runpath = runpath_global.replace("MYMODEL", modelName)
    # if not os.path.isfile(xmlfn): 
    #     xmlfn = "./" + modelName + "_init.xml"
    #     if not os.path.isfile(xmlfn):
    #         raise FileNotFoundError("{}".format(str(xmlfn)))

    mod = ModelicaSystemRunner(
            modelname=modelName,
            runpath=runpath,
        )
    return mod
