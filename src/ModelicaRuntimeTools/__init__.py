import os
import tempfile
import importlib
import json
import pandas as pd
import zipfile
import sys
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


def run_sim_parametric(
        pdf, step_divider=1,
        modelwrapper_name=None, model_name=None,
        res_vars=None,
        use_local=True, modelicaSystemRunner=None, onerr='raise') -> pd.DataFrame:
    """Simulation of a single run. The unique run identifier is in the column run_key."""
    if modelicaSystemRunner is not None:
        mod = modelicaSystemRunner
    else:
        if use_local:
            modelwrapper = importlib.import_module(modelwrapper_name)
            mod = modelwrapper.instantiatemodel(model_name)
        else:
            modelwrapper = importlib.import_module(modelwrapper_name)
            mod = modelwrapper.instantiatemodel(model_name, use_local=False)
    log_str = ''
    if not 'run_key' in pdf.columns:  # Handle weird pandas behavior
        return
    print("Group: {}".format(pdf['run_key'].iloc[0]))
    if 'time' in pdf.columns:
        pdf = pdf.sort_values('time').reset_index()
        pdf['time'] = (pdf['time'] - pdf['time'].iloc[0]) #* 1.0e-9
    print(pdf.head(5))
    temp_dir = tempfile.gettempdir()
    grp = pdf['run_key'].iloc[0]
    resfilename = mod.modelName + '_' + grp + '.mat'
    resfilepathname = os.path.join(temp_dir, resfilename)
    # mod.setParameters(pdf['modifiers'].iloc[0])  # Seems to be not implemented in OMPython
    # We might need to encode the dictonary as json when using pyspark
    stopTime_overridden = False
    if 'modifiers' in pdf.columns:
        overridevariables = json.loads(pdf['modifiers'].iloc[0])
        if len(overridevariables) > 0:
            if 'override_variables' in overridevariables:
                override_variables = overridevariables['override_variables']
                if len(override_variables) > 0:
                    mod.setParameters(**override_variables)
            if 'sim_options_override' in overridevariables:
                sim_options_override = overridevariables['sim_options_override']
                if len(sim_options_override) > 0:
                    if 'stopTime' in sim_options_override:
                        stopTime_overridden = True
                        stopTime = sim_options_override['stopTime']
                    mod.setSimulationOptions(**sim_options_override)
        pdf.drop('modifiers', axis=1, inplace=True)
    else:
        overridevariables = None
    inputs_required = set(mod.getInputs().keys())
    if len(inputs_required) > 0:
        inputs_available = set(pdf.columns)
        if inputs_available.intersection(inputs_required) != inputs_required:
            raise ValueError(
                'The required input series not provided in the DataFrame.\nRequired: {0}. Provided:{1}'.format(
                    str(inputs_required), str(inputs_available)
                )
            )
        # print(str(['time']+list(mod.getInputs().keys())))
        pdf = pdf[['time']+list(mod.getInputs().keys())]
        # Write csv file and tell the model class
        mod.csvFile = os.path.join(temp_dir, mod.modelName + '_' + grp + '_inputs.csv')
        print("Dropping CSV to {}".format(str(mod.csvFile)))
        pdf.to_csv(mod.csvFile, sep=',', lineterminator=',\n')
        print("Dropped CSV")
        mod.inputFlag = True
        if not stopTime_overridden:
            stopTime = float(pdf['time'].max())
        print(f"Starting Sim. stopTime={stopTime}, ")
        # Run the simulation
        numberOfIntervals = len(pdf)
        stepSize = pdf['time'].diff().min() #  0.2
        simOptions = mod.getSimulationOptions()
        simOptions['stopTime'] = stopTime
        simOptions['stepSize'] = stepSize / step_divider
        #optimizationOptions['numberOfIntervals'] = numberOfIntervals
        mod.setSimulationOptions(simOptions)
        log_str += str(mod.simulate(
            resultfile=resfilepathname,
            simflags=None,
            overrideaux='variableFilter="'+'|'.join(list(res_vars))+'"'
            #overrideaux='stopTime={0},'.format(stopTime) +'numberOfIntervals={0},stepSize={1},'.format(numberOfIntervals, stepSize) + 'variableFilter="'+'|'.join(res_vars)+'"'  # TODO numberOfIntervals
        ))
    else:
        # Run the simulation
        log_str += str(mod.simulate(
            resultfile=resfilepathname,
            simflags=None
        ))
    print("Log:")
    print(log_str)
    if len(mod.csvFile) > 0:
        os.remove(mod.csvFile)
    # Collect results
    if isinstance(res_vars, tuple):
        res_vars = list(res_vars)
    try:
        dm = DyMat.DyMatFile(resfilepathname)
        ts_df = dymat2pandas(dm, 2, res_vars)
        #os.remove(resfilepathname)
    except Exception as e:
        err_str = "Cannot load simulation results. SIMLOGSTR:" + log_str + " \nException:" + str(e)
        if onerr == 'raise':
            raise ValueError(err_str)
        elif onerr == 'log':
            log_str = err_str
        ts_df = pd.DataFrame(columns=['time'] + res_vars, data=[(1 + len(res_vars))*[0.0]])
    ts_df.columns = ['time'] + res_vars
    ts_df['run_key'] = grp
    if onerr == 'log':
        ts_df = pd.concat([ts_df, pd.DataFrame(columns=['logmsg'], data=[[log_str]])], axis=1)
        ts_df['logmsg'] == ''
        ts_df['logmsg'].iloc[0] == log_str
    # print(ts_df.head(3))
    return ts_df


def get_sim_dist_func(
        modelwrapper, modelname,
        run_fun=run_sim_parametric, res_vars=None, step_divider=1,
        use_local=True, modelicaSystemRunner=None):
    """Return the pandas (udf) function to simulate a set of runs."""
    modelwrapperName = modelwrapper.__name__
    def run_sim_dist(pdf) -> pd.DataFrame():
        return run_fun(
            pdf,
            modelwrapper_name=modelwrapperName, model_name=modelname, res_vars=res_vars,
            use_local=use_local, modelicaSystemRunner=modelicaSystemRunner, step_divider=step_divider,
        )
    return run_sim_dist
