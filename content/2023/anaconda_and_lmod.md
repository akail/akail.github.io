Title: Integrating Anaconda with Lmod
Date: 2023-08-22 12:00
Category: HPC,Python
Tags: hpc,anaconda
Authors: Andrew Kail

In a previous [post]({filename}/2023/anaconda_init_performance.md) I looked into performance issues with Anaconda initialization.  To
get around users modifying their `.bashrc` and breaking their environment, 
I have instead written an Lmod modulefile that handles setting and unsetting the variables and
fuctions it needs.  This works for both bash and csh.

    #!lua

    -- Point to where your anaconda root directory is
    local root = "/data/apps/anaconda/2022.11/"

    prepend_path("MANPATH", pathJoin(root, "man"))
    prepend_path("MANPATH", pathJoin(root, "share/man"))
    prepend_path("PATH", pathJoin(root, "bin"))
    prepend_path("PATH", pathJoin(root, "sbin"))
    prepend_path("PKG_CONFIG_PATH", pathJoin(root, "lib/pkgconfig"))
    
    prepend_path("PATH", root)
    
    -- Execute existing shell source files
    execute{cmd="source " .. root .. "/etc/profile.d/conda."..myShellType(), modeA={"load"}}
    
    -- This happens at unload for csh
    if (myShellType() == "csh") then
      -- csh sets these environment variables and an alias for conda
      cmd = "unsetenv CONDA_EXE; unsetenv _CONDA_ROOT; unsetenv _CONDA_EXE; unsetenv CONDA_PYTHON_EXE; " ..
            "unsetenv CONDA_SHLVL; unalias conda"
      execute{cmd=cmd, modeA={"unload"}}
    end
    
    -- This happens at unload for Bash
    if (myShellType() == "sh") then
      -- bash sets environment variables, shell functions and path to condabin
      if (mode() == "unload") then
        remove_path("PATH", pathJoin(root,"condabin"))
      end
      cmd = "conda deactivate; " ..
            "unset CONDA_EXE; unset _CE_CONDA; unset _CE_M; " ..
            "unset -f __conda_activate; unset -f __conda_reactivate; " ..
            "unset -f __conda_hashr; unset CONDA_SHLVL; unset _CONDA_EXE; " ..
            "unset _CONDA_ROOT; unset -f conda; " ..
            "unset CONDA_PYTHON_EXE;"
      execute{cmd=cmd, modeA={"unload"}}
    end

Users can even add the `module load anaconda` to their bashrc safely as this will initialize
anaconda without the penalty of running the `__conda_setup` function from the last article.

This also has the added benefit of allowing for multiple Anaconda installations in single environment
as a users `.bashrc` will not point to a hard-coded location.
