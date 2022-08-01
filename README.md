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
Where `run_func` is a Python function which serves as an ***entry point*** to the Modelica model or package. It
- Gets a pandas dataframe of input data for a single run.
- Drops the input data as a file in the (local) temporary directory
- Optionally compiles the model executable if the structure of the model is dynamically changeable
- Calls the model executable which drops the simulation results in the (local) temporary directory
- Reads the simulation results and returns them as a pandas dataframe.

Finally, the model can be deployed on a ***cluster*** as a conda package for large scale analytics.

## Entry point
The *entry point* is a small Python package which is placed next to the Modelica package.
```python
# Running the parametric simulation
ts_sim_df = input_df.groupby(['run_key']).applyInPandas(
        get_sim_func(EDrives, 'BouncingBall', res_vars=['h', 'v']), schema=res_schema
    )
```
where `EDrives` is a Python package that serves as an entry point to the model with a fixed relative location next to `package.mo`.

It implements the following methods:
- `create_mos_file()` to create a Modelica script file to build the models.
- `run_mos_file()` to call `omc` with the Modelica script file and return stdout and stderr. The result is the models executables with the `modelNames_init.xml` files.
- `instantiatemodel('BouncingBall')` to instantiate OMPython's `ModelicaSystem` with the parameter `xmlFileName` which tells ModelicaSystem to use the pre-build model as described in `BouncingBall_init.xml`.

## Demo examples
- [BouncingBall](notebooks/BouincingBall/README.md) is one of the most simple and famous Modelica examples.
- EDrives, is a more complex example of a package that depends on the [Modelica Standard Library](https://github.com/modelica/ModelicaStandardLibrary).

## Deploying the models on a cluster using conda
[Anaconda](https://anaconda.org) is the "The World's Most Popular Data Science Platform" and the [OpenModelica compiler is available as a conda package](https://anaconda.org/conda-forge/omcompiler) too. `conda-build` is used to create a conda package of the model according to the recipe from [`meta.yaml`](conda_recipe/meta.yaml) and [`setup.py`](src/setup.py).

OpenModelica provides its own [package manager](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/packagemanager.html) enabling the installation of Modelica libraries in a mo-script via `installPackage`. For example `installPackage(Modelica, "3.2.3");` will download and install the Modelica Standard library 3.2.3 on the local system. Unfortunately, the usage of this package manager might not be appropriate in a cloud computing cluster environment.

Consequently, the Modelica libraries must be available as conda packages too. This [recipe](https://github.com/joewa/staged-recipes/blob/main/recipes/omsl/meta.yaml) creates a conda package of the OpenModelica-Standard-Library.

So this is the challenge:
- Build a conda package of model on (or for) the target platform once using [`conda-build`](https://docs.conda.io/projects/conda-build/en/latest/index.html) and deploy it on a cluster.
- Run the model on scale or in production with massive input data.

## Building and installing the conda package
Go to the `conda-recipe` and run

    conda-build . -c conda-forge --output-folder ./build

or

    conda-build . -c conda-forge --python=3.9 --output-folder ./build

if you want to build for a version of Python different to your actual environment. This will create a subdirectory `build` that contains the package.

To install the package in an existing environment, run:

    conda install pymodelicademo -c ./build

or to create a fresh environment, `packtest`, run:

    conda create -n packtest python=3.9 pymodelicademo -c ./build

or to create a fresh environment that has matplotlib and Jupyterlab for the notebooks, run:

    conda create -n packtest python=3.9 jupyterlab pyarrow matplotlib pymodelicademo -c ./build

## Workflow
- The development of a model and the required analytics is done a conda environment `modelicadevenv` which has `omcompiler`, `pandas` and your favourite conda packages to develop interactively.
    - For the BouncingBall example, see the notebook [dev_interactive_omc.ipynb)](notebooks/BouncingBall/dev_interactive_omc/dev-interactive-omc.ipynb).
    - For the EDrives example, see the notebook [dev_interactive_omc.ipynb)](notebooks/EDrives/dev_interactive_omc/dev-interactive-omc.ipynb).
- Create a [recipe](conda_recipe/meta.yaml), build a package using `conda-build` and create a fresh environment that contains the package. Building packages and creating fresh environments will take a while. Do it only when you have seen thing working in `modelicadevenv`.
- Activate the fresh environment and test the package.
    - For the BouncingBall example, see the notebook [test_integration.ipynb)](notebooks/BouncingBall/test_integration.ipynb) and the script [test_pandas.py](notebooks/BouncingBall/test_pandas.py).
- Deploy in the cluster...

## Future work
- Creation of more conda packages from useful tools and Modelica libraries and distribution through [conda-forge](https://conda-forge.org/), e.g.
    - OMPython
    - DyMat
    - Modelica Standard library
    - ...
- Provide more examples, e.g. for building models on runtime on a cluster.
