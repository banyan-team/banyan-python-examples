# Banyan Python Examples

This repo contains examples and tutorials for various Banyan Python libraries.

## Running the Example Notebooks

To run the notebooks, follow the following steps:

1. Set up a Banyan account by following the steps [here](https://www.banyancomputing.com/getting-started/).
2. [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and clone (download) this repository by running the following in a terminal (command prompt):

```
git clone git@github.com:banyan-team/banyan-python-examples.git
```

3. Download the Python installer for your operating system [here](https://www.python.org/downloads/), and follow the instructions to finish the installation. Be sure to select a version >= 3.8.

4. Install Jupyter Notebook by running `pip install notebook` or follow directions [here](https://jupyter.org/install).

5. Cd into the directory of the notebook you would like to run. Then, run `BANYAN_API_KEY=<YOUR_BANYAN_API_KEY>   BANYAN_USER_ID=<YOUR_BANYAN_USER_ID> poetry run jupyter notebook` to open Jupyter Notebook in the required environment. Then open the `.ipynb` file to run the notebook. Alternatively, you can open the notebooks in VSCode, following the instructions[here](https://hippocampus-garden.com/jupyter_poetry_pipenv/).


## Summary of Notebooks

- [`flow_simulation.ipynb`](/flow_simulation/flow_simulation.ipynb) - This notebook provides an example of how to spin up a cluster and a session and how to run an MPI-based water flow simulation on the cluster.
