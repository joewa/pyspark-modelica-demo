# pyspark-modelica-demo
Demonstration of the usage of pyspark &amp; pandas to run Modelica models on scale.

## Background
Apache Spark, particularly Pyspark, became the Foundation to run Big Data analytics and heavy machine learning tasks on scalable computation clusters. OpenModelica enables the simulation of physics and systems in the real world real world using (differential-algebraic) equations and discrete events.

In a nutshell, the idea of this demo is:
- Provide groups (or runs) of input data as a Spark DataFrame, `input_df`, (e.g. timeseries and/or parameters) to Modelica models.
- Then execute the simulation model for each group of data in parallel.
- Finally collect the resulting timeseries in a Spark DataFrame again.
This can be achieved with the follwing pattern:
```python
ts_sim_df = input_df.groupby(['run_key']).applyInPandas(run_func, schema=r)
```
Where `run_func` is a Python function which:
- Gets a pandas dataframe of input data for a single run.
- Drops the input data as a file in the (local) temporary directory
- Optionally compiles the model executable if the structure of the model is dynamically changeable
- Calls the model executable which drops the simulation results in the (local) temporary directory
- Reads the simulation results and returns them as a pandas dataframe.

## A simple example
This is the model of a bouncing ball:
```modelica
model BouncingBall
  parameter Real e=0.7 "coefficient of restitution";
  parameter Real g=9.81 "gravity acceleration";
  Real h(fixed=true, start=1) "height of ball";
  Real v(fixed=true) "velocity of ball";
  Boolean flying(fixed=true, start=true) "true, if ball is flying";
  Boolean impact;
  Real v_new(fixed=true);
  Integer foo;

equation
  impact = h <= 0.0;
  foo = if impact then 1 else 2;
  der(v) = if flying then -g else 0;
  der(h) = v;

  when {h <= 0.0 and v <= 0.0,impact} then
    v_new = if edge(impact) then -e*pre(v) else 0;
    flying = v_new > 0;
    reinit(v, v_new);
  end when;
end BouncingBall;
```
So the model has two parameters (the coefficient of restitution, e and the gravity accesleration, g) and no timeseries inputs. The challenge could be a parametric simulation with the following input data.
```python
# Running the parametric simulation
ts_sim_df = input_df.groupby(['run_key']).applyInPandas(
        get_sim_func(BouncingBall, res_vars=['h', 'v']), schema=res_schema
    )
```

## Deploying jobs in a cloud computing platform using conda
[Anaconda](https://anaconda.org) is the "The World's Most Popular Data Science Platform" and the [OpenModelica compiler is available as a conda package](https://anaconda.org/conda-forge/omcompiler) too.

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

