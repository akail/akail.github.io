Title: Ansible Operations in an HPC MSP
Date: 2101-01-01 12:00
Category: HPC
Tags: ansible,hpc
Authors: Andrew Kail

## Background
As a Managed Services Provider in the HPC space we have started to look for
ways to leverage ansible to help with scaling up our management and operations
of the cluster under our purview. We have seen great success in this initiative
with our efforts to deploy a HPC focused monitoring stack.

In the process though, we have gone from one engineer running ansible to the need
for multiple engineers.

As of now, the ansible roles are in a centralized git repository
that is then shared as a submodule to individual client repositories.

We have found that with more engineers there is an increased likelihood of an engineer
making a change to the repository in their home space our on their workstation and
neglect to commit and/or push the changes up to github, while another engineer may also
neglect to pull changes before running their commits.  While we have yet to truly
run into this problem, we want to be proactive in our workflow and establish some 
sort of best practice.

Unfortunately research into this space has shown the most straightforward option
is to run [Ansible Tower](https://www.ansible.com/products/controller) or its upstream open source project
[AWS](https://github.com/ansible/awx).  Unfortunately, Tower is prohibitively expensesive for our clients
who are usually running under lean budgets, and AWS is a massive pain to install
requiring K8s. Other similar options exist with RBAC controls like Rundeck and Semaphore,
but lack some features we would like. 

We have since looked for a more command line driven solution

**Requirements**

* Local to the cluster
* 


## Deploy Key User


**Pros**
* Forces all ansible to be run from a central place
* 

**Cons**
* 

## Running Individually

**Pros**
* 

**Cons**
* 
