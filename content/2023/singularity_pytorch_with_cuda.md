Title: Simple Nvidia PyTorch Container
Date: 2023-09-06 00:00
Category: Python
Tags: apptainer,jupyter,nvidia,pytorch
Authors: Andrew Kail

Another quick Apptainer example for getting pytorch quickly up and
running.

**The Definition File**

    :::singularity
    Bootstrap: docker
    From: nvidia/cuda:11.7.1-runtime-ubuntu22.04

    %post
        apt-get -y update
        apt install -y python3 python3-pip
        pip3 install torch torchvision torchaudio
        pip3 install ipykernel


**Build the Contaienr**

    apptainer build pytorch.sif pytorch.def

**Test**

Passing `--nv` tells apptainer to setup apptainer for running with the Nvidia GPU.


    apptainer exec --nv pytorch.sif python3 -c "import torch; print(torch.cuda.is_available())"
    True
