import sys
import pandas as pd

# sys.path.insert(0, '../../src')
from ModelicaRuntimeTools import get_sim_dist_func
from MM import BouncingBall


def run_bouncingball_pandas(parameters_var_df) -> pd.DataFrame:
    # Running the parametric simulation
    # 1. Duplicate the column to act as the grouping key
    parameters_var_df['_group_key'] = parameters_var_df['run_key']
    # 2. Group by the shadow column instead
    ts_all_df = parameters_var_df.groupby(['_group_key']).apply(
            get_sim_dist_func(BouncingBall, 'BouncingBall', res_vars=['h', 'v'])
        )
    if '_group_key' in ts_all_df.columns:
        ts_all_df = ts_all_df.drop(columns=['_group_key'])
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
            get_sim_dist_func(BouncingBall, 'BouncingBall', res_vars=['h', 'v']), schema=res_schema
        )
    return ts_all_df
