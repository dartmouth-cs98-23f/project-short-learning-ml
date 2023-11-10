# Short Form Learning - Machine Learning

This repository contains all things machine learning for the short-form learning project.

## Architecture

- [`app/`](./app/) contains the FastAPI application.
- [`archive/`](./app/) contains old code that is no longer used.

## Setup

We use [`conda`][conda] for Python package management.

### Installing `conda`

First, check if you have `conda` installed on your machine:

```bash
conda --version
# if you get an error, you do not have conda installed
```

To install `conda`, follow the instructions [here][conda-install].

### Installing the environment

The environment is defined in [`environment.osx.yml`][env1] for MacOS
and [`environment.linux.yml`][env2] for Linux.  
To install the environment, run:

```bash
conda env create -f environment.<platform>.yml
```

> [!IMPORTANT]
> Make sure you pick the right platform,
> because specific libraries (such as [`libgfortran`][libgfortran])
> have different targets for different platforms.

### Running the App

The app is structured as a FastAPI application.
To launch the app (assuming all dependencies)

## Deployment

1. Running `docker build -t discite .` will build the docker image.
2. You can then deploy the image on a server if you wish to.

TODO: add live demo link

<!-- TODO: how to deploy the project -->

## Authors

Team Discite.

## Acknowledgments

[env1]:           environment.osx.yml
[env2]:           environment.linux.yml
[conda]:          https://docs.conda.io
[conda-install]:  https://docs.conda.io/projects/conda/en/latest/user-guide/install/
[libgfortran]:    https://anaconda.org/conda-forge/libgfortran
