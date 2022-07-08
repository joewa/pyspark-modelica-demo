import sys
import pandas as pd

# sys.path.insert(0, '../../src')
from ModelicaRuntimeTools import get_sim_dist_func
from ModelicaModels import BouncingBall


def run_bouncingball_pandas(parameters_var_df) -> pd.DataFrame:
    # Running the parametric simulation
    ts_all_df = parameters_var_df.groupby(['run_key']).apply(
            get_sim_dist_func(BouncingBall, res_vars=['h', 'v'])
        )
    return ts_all_df


def run_bouncingball_spark(parameters_var_df):
    from pyspark.sql import types as T
    res_schema = T.StructType([
        T.StructField("time", T.DoubleType(), True),
        T.StructField("h", T.DoubleType(), True),
        T.StructField("v", T.DoubleType(), True),
        T.StructField("run_key", T.StringType(), True),
    ])
    # Running the parametric simulation
    ts_all_df = parameters_var_df.groupby(['run_key']).applyInPandas(
            get_sim_dist_func(BouncingBall, res_vars=['h', 'v']), schema=res_schema
        )
    return ts_all_df
