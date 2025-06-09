import os
import sys
import pathlib
import subprocess
import pkg_resources
from OMPython import ModelicaSystem


modelName = "BouncingBall"
fn = pkg_resources.resource_filename(__name__, "BouncingBall.mo")
mosfn = fn + 's'
# xmlfn_global = pkg_resources.resource_filename(
#         __name__,
#         os.path.join("..", "build") + "/" + modelName + "_init.xml"
#     )
runpath_global = pkg_resources.resource_filename(
        __name__,
        os.path.join("..", "build")
    )


def create_mos_file():
    mos_file = open(mosfn, 'w', 1)
    mos_file.write('loadFile("' + fn + '");\n')
    # mos_file.write('setComponentModifierValue(CalledbyPython,b,$Code(="+str(newb)+"));\n')
    mos_file.write('buildModel(' + modelName + ');\n')
    mos_file.close()
    pass


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


def instantiatemodel(modelName, use_local=True, force_executable_path=None):
    if isinstance(use_local, bool):
        if use_local:
            xmlfn = pkg_resources.resource_filename(
                    __name__,
                    os.path.join("..", "build", modelName + "_init.xml")
                )
            runpath = pkg_resources.resource_filename(
                    __name__,
                    os.path.join("..", "build")
                )
            runpath = pathlib.Path(runpath).resolve().absolute()
        else:
            runpath = pathlib.Path(runpath_global).resolve().absolute()
    elif isinstance(use_local, str):
        runpath = pathlib.Path(use_local).resolve().absolute()

    # mod = ModelicaSystem(
    #         fileName=fn, modelName=modelName,
    #         xmlFileName=xmlfn
            
    #     )
    mod = ModelicaSystem(
            # fileName=fn,
            modelName=modelName,
            customBuildDirectory=runpath,
            session='none',
            build=False,
        )
    print(str(runpath))
    return mod
