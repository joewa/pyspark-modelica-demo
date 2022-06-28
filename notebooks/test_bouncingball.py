import pandas as  pd
import os
import sys

import OMPython  # import ModelicaSystem
import DyMat


# sys.path.insert(0, '../src')
# sys.path.insert(0, '/home/joerg/miniforge3/lib/python3.9/site-packages/ModelicaModels/build/BouncingBall/BouncingBall/')


def dymat2pandas(dm, block, names) -> pd.DataFrame:
    ts_df = pd.DataFrame(dm.getVarArray(names)).T
    #ts_df['time'] = dm.abscissa(2)
    ts_df.columns=['time'] + names
    return ts_df


from ModelicaModels import BouncingBall

mod = BouncingBall.instantiatemodel()

sim_options_d = mod.getSimulationOptions()
sim_options_d['stopTime'] = 2
mod.setSimulationOptions(sim_options_d)


print('Default parameters for model Bouncingall')
print(mod.getParameters())

# Paramtric simulation
## Sequential execution (with pandas)

### Definition of model parameters
parameters_var_df = pd.DataFrame(columns=['run_key', 'modifiers'], data=[
    ['r1', ['e=0.7']],
    ['r2', ['e=0.5']],
    ['r3', ['e=0.9']],
])



def run_sim(mod, parameters, res_vars=None, pathname=None) -> pd.DataFrame:
    """Simulation of a single run. The unique run identifier is in the column run_key."""
    grp = parameters['run_key'].iloc[0]
    resfilename = grp + '.mat'
    resfilepathname = os.path.join(pathname, resfilename)
    mod.setParameters(parameters['modifiers'])
    mod.simulate(resultfile=resfilename, simflags=None)
    # Collect results
    if isinstance(res_vars, tuple):
        res_vars = list(res_vars)
    try:
        dm = DyMat.DyMatFile(resfilepathname)
        ts_df = dymat2pandas(dm, 2, res_vars)
    except:
        ts_df = pd.DataFrame(columns=['time'] + res_vars, data=[[-1.0 ,0.0, 0.0]])
    os.remove(resfilepathname)
    ts_df.columns = ['time'] + res_vars
    ts_df['run_key'] = grp
    return ts_df


def get_sim_dist_func(mod, res_vars=None):
    """Return the pandas (udf) function to simulate a set of runs."""
    pathname = os.path.join(os.path.dirname(BouncingBall.__file__), '../build/BouncingBall')
    def run_sim_dist(parameters) -> pd.DataFrame():
        return run_sim(mod, parameters, res_vars=res_vars, pathname=pathname)
    return run_sim_dist


# Running the parametric simulation
ts_all_df = parameters_var_df.groupby(['run_key']).apply(
        get_sim_dist_func(mod, res_vars=['h','v'])
    )
print(ts_all_df)
