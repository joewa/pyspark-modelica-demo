import os
import pkg_resources
from OMPython import ModelicaSystem


modelname = "BouncingBall"
fn = pkg_resources.resource_filename(__name__, "BouncingBall.mo")
mosfn = fn + 's'


def create_mos_file():
    mos_file = open(mosfn, 'w', 1)
    mos_file.write('loadFile("' + fn + '");\n')
    # mos_file.write('setComponentModifierValue(CalledbyPython,b,$Code(="+str(newb)+"));\n')
    mos_file.write('buildModel(' + modelname + ');\n')
    mos_file.close()
    pass


def run_mos_file():
    # r = os.popen("omc " + mosfn).read()
    r = os.popen("omc " + mosfn).readlines()
    return r


def buildmodel():
    # return ModelicaSystem(fileName=fn, modelName=modelname, useCorba=False)
    # return ModelicaSystem(fileName=fn, modelName="BouncingBall", useCorba=True)
    create_mos_file()
    r = run_mos_file()
    return r


def instantiatemodel():
    xmlfn = pkg_resources.resource_filename(__name__, "../build/BouncingBall/BouncingBall_init.xml")
    mod = ModelicaSystem(
            fileName=fn, modelName="BouncingBall",
            xmlFileName=xmlfn
        )
    return mod
