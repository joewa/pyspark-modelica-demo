# pyspark-modelica-demo
Demonstration of the usage of pyspark &amp; pandas to run Modelica models on scale.

## Idea & Background
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

Finally, the model can be deployed on a ***cluster*** as a conda package for large scale analytics.
- Build and compile the model once.
- Create a ***conda*** package.
- Run the compiled model with different input data, e.g. parameters and/or timeseries.
- Use it on scale, deploy it on a cluster. Change parameters only during runtime.

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

## Deploying the models on a cluster using conda
[Anaconda](https://anaconda.org) is the "The World's Most Popular Data Science Platform" and the [OpenModelica compiler is available as a conda package](https://anaconda.org/conda-forge/omcompiler) too. `conda-build` is used to create a conda package of the model according to the recipe from `meta.yaml`.

OpenModelica provides its own [package manager](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/packagemanager.html) enabling the installation of Modelica libraries in a mo-script via `installPackage`. For example `installPackage(Modelica, "3.2.3");` will download and install the Modelica Standard library 3.2.3 on the local system. Unfortunately, the usage of this package manager might not be appropriate in a cloud comuputing cluster environment.

Consequently, the Modelica libraries must be available as conda packages too. For example [recipe](https://github.com/joewa/staged-recipes/blob/main/recipes/omsl/meta.yaml) creates a conda package of the OpenModelica-Standard-Library.

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

## Workflow
- The development of a model and the required analytics is done a conda environment `modelicadevenv` which has `omcompiler`, `pandas` and your favourite conda packages to develop interactively. For the BouncingBall example, see the notebook [dev_interactive_omc.ipynb)](notebooks/BouncingBall/dev_interactive_omc/dev-interactive-omc.ipynb).
- Compile a [recipe](conda_recipe/meta.yaml), build a package using `conda-build` and create a fresh environment that contains the package. Building packages and creating fresh environments will take a while. Do it only when you have seen thing working in `modelicadevenv`.
- Activate the fresh environment and test the package. For the BouncingBall example, see the notebook [test_integration.ipynb)](notebooks/BouncingBall/test_integration.ipynb) and the script [test_pandas.py](notebooks/BouncingBall/test_pandas.py).
- Deploy in the cluster...

## Future work
- Creation of more conda packages from useful tools and Modelica libraries and distribution through [conda-forge](https://conda-forge.org/), e.g.
    - OMPython
    - DyMat
    - Modelica Standard library
    - ...
- Provide more examples, e.g. for building models on runtime on a cluster.
