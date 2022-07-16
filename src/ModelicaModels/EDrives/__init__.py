import os
import pkg_resources
from OMPython import ModelicaSystem


# modelName = "EDrives.Examples.DCDC.DC_Drive_Switching"
fn = pkg_resources.resource_filename(
    __name__,
    os.path.join("EDrives", "package.mo")
    )

def get_mosfn(modelName):
    return pkg_resources.resource_filename(
        __name__,
        modelName + ".mos"
        )

xmlfn_global = pkg_resources.resource_filename(
        __name__,
        os.path.join("..", "build", "MYMODEL") + "/" + "MYMODEL" + "_init.xml"
    )


def create_mos_file(mofile, modelName, mosfn, install_msl=False, load_msl=False):
    mos_file = open(mosfn, 'w', 1)
    if install_msl:
        # TODO: check if already installed
        mos_file.write('installPackage(Modelica, "3.2.3");')
        mos_file.write('getErrorString();')
    if load_msl:
        mos_file.write('loadModel(Modelica);\n')
        mos_file.write('getErrorString();')
    mos_file.write('loadFile("' + mofile + '");\n')
    mos_file.write('getErrorString();')
    # mos_file.write('setComponentModifierValue(CalledbyPython,b,$Code(="+str(newb)+"));\n')
    mos_file.write('buildModel(' + modelName + ');\n')
    mos_file.write('getErrorString();')
    mos_file.close()
    pass


def run_mos_file(mosfn):
    # r = os.popen("omc " + mosfn).read()
    r = os.popen("omc " + mosfn).readlines()
    return r


def buildmodel(modelName):
    mosfn = get_mosfn(modelName)
    create_mos_file(fn, modelName, mosfn, load_msl=True)
    r = run_mos_file(mosfn)
    return r


def instantiatemodel(modelName, use_local=True):
    if use_local:
        xmlfn = pkg_resources.resource_filename(
                __name__,
                os.path.join("..", "build", modelName) + "/" + modelName + "_init.xml"
            )
    else:
        xmlfn = xmlfn_global.replace("MYMODEL", modelName)
    mod = ModelicaSystem(
            fileName=fn, modelName=modelName,
            xmlFileName=xmlfn
        )
    return mod
