Title: Running A Jupyter Kernel In Apptainer
Date: 2023-08-30 00:00
Category: Python
Tags: apptainer,jupyter
Authors: Andrew Kail

Just a quick example of running a Jupyter kernel inside an ~~Singularity~~ 
Apptainer container.

First define a container with all the required applications, in particular `ipykernel`.

    :::singularity
    bootstrap: docker
    From: python:3.11-slim-buster

    %runscript
        echo "Hello... I am a new Singularity container"

    %labels
        AUTHOR andrew@kail.io

    %post
        apt-get update && apt-get install -y python-pip python-dev build-essential
        pip install --upgrade pip
        pip install numpy
        pip install ipykernel


Build the container image.

    :::bash
    apptainer build ipykernel.sif ipykernel.def

Finally, add the following to kernel specification under `/home/<user>/.local/share/jupyter/kernels/<kernelname>/kernel.json`

    :::json
    {
     "argv": [
       "singularity",
       "exec",
       "--cleanenv",
       "/home/akail/Projects/singularity/kernel/ipykernel.sif",
       "python",
       "-m",
       "ipykernel",
       "-f",
       "{connection_file}"
     ],
     "language": "python",
     "display_name": "singularity-kernel"
    }
    
Restart Jupyter or Jupyter lab and you're all set.
