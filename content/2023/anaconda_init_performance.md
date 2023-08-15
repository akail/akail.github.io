Title: Performance Impact of Anaconda Initialization
Date: 2023-08-15 12:00
Category: HPC,Python
Tags: hpc,slurm,anaconda
Authors: Andrew Kail


One of the biggest complaints we get from many users is a delayed login when they initially
get into the cluster.  In most cases, we have narrowed it down to users either installing
their own version of [Anaconda](https://anaconda.org) or they're using an existing install
without without a customized modulefile.

The cause of this is conda requiring environment variables and fuctions be defined in order
for it to function.  Usually a user will be asked to run `conda init` when these variables do not exist.  On linux in bash, it adds the following to the users `.bashrc`.

    #!bash 
    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('/data/apps/anaconda/3.9/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
    else
        if [ -f "/data/apps/anaconda/3.9/etc/profile.d/conda.sh" ]; then
            . "/data/apps/anaconda/3.9/etc/profile.d/conda.sh"
        else
            export PATH="/data/apps/anaconda/3.9/bin:$PATH"
        fi
    fi
    unset __conda_setup
    # <<< conda initialize <<<


The issue on our systems has been line 5, where the conda python executable is called every time the the user logs in.  Essentially every time the user logs in conda is called to generate the proper environment variables.  This launches python, loads conda and other libraires, and possibly writes many `.pyc` files depending on where anaconda is installed.

Using the python trace module, we can see how many files are accessed.

    :::bash linenums=True
    mkdir cover; cd cover
    python -m trace -c -C /data/apps/anaconda/3.9/bin/conda shell.bash hook
    # Get the number of files generated
    ls -al | wc -l

This will generate a `.cover` file for each python file that is executed.  In this particular case I had 146 Python files executed.  While this doesn't mean that each file was actually used, in Python, each file is read and byte compiled when imported if not already done so.  Thankfully most of these are byte compiled already so there shouldn't bee too many writes, just a few reads. Depending on the filesystem, such as a parallel filesystem, this could be less performant if on a shared filesystem.  Many small file access has always been a little problematic for us, even with some optimizations.

For some empirical measurement on a cluster we know this is a problem I ran an ssh test from a local node 10 times with and 10 times without call the `__conda_setup`, both ending up with the same environment configuration.

    :::bash linenums=True
    time ssh login uptime

|      | SSH Setup Call | SSH Direct Source |
| --   | --             | --                |
| Min  | 8.8936         | 3.562             |
| Max  | 10.049         | 4.558             |
| Mean | 9.7646         | 4.0282            |


I also took a look at the timing for running the setup directly and got the following times:

|      | Local Setup |
| --   | --          |
| Min  | 2.324       |
| Max  | 4.199       |
| Mean | 3.2227      |

Now, there are a few caveats about my tests above I noticed when taking a look at performance on other nodes:

1. This login node is very busy with a lot of small IO operations in progress
2. There is an existing performance issue on this file system client

Looking at another server in the same cluster I got the following timing profiles:

|      | SSH Setup Call | SSH Direct Source | Local Setup |
| --   | --             | --                | --          |
| Min  | 3.582          | 2.256             | 0.396       |
| Max  | 5.548          | 3.284             | 0.884       |
| Mean | 4.2926         | 2.7692            | 0.516       |

While definitely better than the login node, there is still a 1-2 second performance hit when doing the conda setup over ssh. 

On my local machine the performance for local setup matches that of the second node above and definitely more consistent.


|      | Local Setup |
| --   | --          |
| Min  | 0.17        |
| Max  | 2.14        |
| Mean | 0.1797      |


I'm going to continue to look into why the `__conda_setup` call takes up to 3 times longer over ssh as opposed to being run locally. 
I have a feeling there is something else going on under the hood and there may be a way to squeak out better performance.

I'm a little confused though by the auto-generated initialization above.  By default, it executes conda to generate the environment variables and if that fails, it then sources a pre-generated file directly without executing any python code.  I would recommend it instead attempt to source the files directly first then fall back to generating the bash initialization after that.   I'm sure the Anaconda developers have their reason for doing it in that order but it just doesn't seem necessary to me.

In my opinion the performance hit over ssh is more than I care for and I wish conda did not require this in order to properly function.  Our recommendation  to prevent this is to use a centrally managed 
anaconda install with a custom modulefile to manage these environment variables, then follow up with the users to make sure they're `.bashrc` files are cleaned up.

I'll be following up this article with a brief look at a modulefile to handle this on HPC clusters using Lmod.
