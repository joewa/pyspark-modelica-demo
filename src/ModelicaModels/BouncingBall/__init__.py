import os
import pkg_resources
from OMPython import ModelicaSystem


modelName = "BouncingBall"
fn = pkg_resources.resource_filename(__name__, "BouncingBall.mo")
mosfn = fn + 's'
xmlfn_global = pkg_resources.resource_filename(
        __name__,
        os.path.join("..", "build", modelName) + "/" + modelName + "_init.xml"
    )


def create_mos_file():
    mos_file = open(mosfn, 'w', 1)
    mos_file.write('loadFile("' + fn + '");\n')
    # mos_file.write('setComponentModifierValue(CalledbyPython,b,$Code(="+str(newb)+"));\n')
    mos_file.write('buildModel(' + modelName + ');\n')
    mos_file.close()
    pass


def run_mos_file():
    # r = os.popen("omc " + mosfn).read()
    r = os.popen("omc " + mosfn).readlines()
    return r


def buildmodel(modelName):
    # return ModelicaSystem(fileName=fn, modelName=modelname, useCorba=False)
    # return ModelicaSystem(fileName=fn, modelName="BouncingBall", useCorba=True)
    create_mos_file()
    r = run_mos_file()
    return r


def instantiatemodel(modelName, use_local=True):
    if use_local:
        xmlfn = pkg_resources.resource_filename(
                __name__,
                os.path.join("..", "build", modelName) + "/" + modelName + "_init.xml"
            )
    else:
        xmlfn = xmlfn_global
    if not os.path.isfile(xmlfn): 
        xmlfn = "./" + modelName + "_init.xml"
        if not os.path.isfile(xmlfn):
            raise FileNotFoundError("{}".format(str(xmlfn)))
    mod = ModelicaSystem(
            fileName=fn, modelName=modelName,
            xmlFileName=xmlfn
        )
    return mod
