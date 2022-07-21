# pyspark-modelica-demo
Demonstration of the usage of pyspark &amp; pandas to run Modelica models on scale.

## Background
Apache Spark, particularly Pyspark, became the Foundation of Big Data analytics and machine learning.
Clusters. Simulation.
```python
# Running the parametric simulation
ts_sim_sdf = parameters_var_sdf.groupby(['run_key']).applyInPandas(
        get_sim_dist_func(BouncingBall, res_vars=['h', 'v'], use_local=True), schema=res_schema,
    ).cache()
```

## Building and installing the conda package
Go to the `conda-recipe` and run

    conda-build . -c conda-forge --output-folder ./build

or

    conda-build . -c conda-forge --python=3.9 --output-folder ./build

if you want to build for a version of Python different to your actual environment. This will create a subdirectory `build` that contains the package.

To install the package in an existing environment, run:

    conda install pymodelicademo -c ./build

or to create a fresh environment, `modelicatestenv`, run:

    conda create -n modelicatestenv python=3.9 pymodelicademo -c ./build

or to create a fresh environment that has matplotlib and Jupyterlab for the notebooks, run:

    conda create -n packtest python=3.9 jupyterlab pyarrow matplotlib pymodelicademo -c ./build

