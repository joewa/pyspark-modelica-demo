import os
import tempfile
import importlib
import json
import pandas as pd
import zipfile
import DyMat


# Platform helper functions
def zipdir(basedir, z, MODULE_EXTENSIONS, dironly=False):
    assert os.path.isdir(basedir)
    if dironly:
        rootdir = os.path.basename(os.path.normpath(basedir))
    else:
        rootdir = ''
    for root, dirs, files in os.walk(basedir):
        for fn in files:
            if fn.endswith(MODULE_EXTENSIONS):
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):]  # relative path
                if len(rootdir) > 0:
                    zfn = os.path.join(rootdir, zfn)
                # print(zfn)
                z.write(absfn, zfn)


def addpymodules(modules_list, zipfilename, out_dir='.', MODULE_EXTENSIONS=('.py'), sc=None, dironly=False):
    """Create zip-file of Python moodules and add them to os.path and sc"""
    f = os.path.join(out_dir, zipfilename)
    zipf = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    for package in modules_list:
        zipdir(package, zipf, MODULE_EXTENSIONS, dironly=dironly)
    zipf.close()

    if f not in sys.path:
        sys.path.insert(0, f)
    if sc is not None:
        sc.addPyFile(f)


# Helper functions for running a model
def dymat2pandas(dm, block, names) -> pd.DataFrame:
    ts_df = pd.DataFrame(dm.getVarArray(names)).T
    #ts_df['time'] = dm.abscissa(2)
    ts_df.columns=['time'] + names
    return ts_df


def run_sim_parametric(parameters, modelwrapper_name=None, res_vars=None, use_local=True) -> pd.DataFrame:
    """Simulation of a single run. The unique run identifier is in the column run_key."""
    if use_local:
        modelwrapper = importlib.import_module(modelwrapper_name)
        mod = modelwrapper.instantiatemodel()
    else:
        mod = instantiatemodel(use_local=False) 
    log_str = ''
    print(parameters)
    temp_dir = tempfile.gettempdir()
    grp = parameters['run_key'].iloc[0]
    resfilename = grp + '.mat'
    resfilepathname = os.path.join(temp_dir, resfilename)
    # mod.setParameters(parameters['modifiers'].iloc[0])  # Seems to be not implemented in OMPython
    # We might need to encode the dictonary as json when using pyspark
    mod.overridevariables = json.loads(parameters['modifiers'].iloc[0])
    log_str += str(mod.simulate(resultfile=resfilepathname, simflags=None))
    # Collect results
    if isinstance(res_vars, tuple):
        res_vars = list(res_vars)
    try:
        dm = DyMat.DyMatFile(resfilepathname)
        ts_df = dymat2pandas(dm, 2, res_vars)
        os.remove(resfilepathname)
    except Exception as e:
        ts_df = pd.DataFrame(columns=['time'] + res_vars, data=[[-1.0 ,0.0, 0.0]])
    ts_df.columns = ['time'] + res_vars
    ts_df['run_key'] = grp
    # print(ts_df.head(3))
    return ts_df


def get_sim_dist_func(modelwrapper, run_fun=run_sim_parametric, res_vars=None, use_local=True):
    """Return the pandas (udf) function to simulate a set of runs."""
    modelwrapperName = modelwrapper.__name__
    def run_sim_dist(parameters) -> pd.DataFrame():
        return run_fun(
            parameters,
            modelwrapper_name=modelwrapperName, res_vars=res_vars,
            use_local=use_local
        )
    return run_sim_dist
