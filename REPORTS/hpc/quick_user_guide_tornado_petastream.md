---
title: "Quick User Guide: Polytechnik - RSK Tornado and RSK Petastream Computing Clusters"
source_file: "user_man_tornado_ps-short.pdf"
language: "ru"
converted_on: "2026-05-12"
---

# Quick User Guide for the "Polytechnik - RSK Tornado" and "Polytechnik - RSK Petastream" Computing Clusters

## Contents

1. [Available Resources](#1-available-resources)
2. [Access to Resources](#2-access-to-resources)
3. [Creating SSH Keys](#3-creating-ssh-keys)
   - 3.1. Creating SSH Keys on Unix Systems
   - 3.2. Creating SSH Keys on Windows Systems
4. [Environment Setup](#4-environment-setup)
5. [Running Jobs](#5-running-jobs)

---

## 1. Available Resources

Users of the SCC "Polytechnichesky" currently have access to the following computing resources:

- **612 nodes** of the "Polytechnik - RSK Tornado" cluster (hereinafter tornado nodes)
  - 2 × Intel Xeon CPU E5-2697 v3 @ 2.60GHz
  - 64 GB RAM

- **56 nodes** of the "Polytechnik - RSK Tornado" cluster with NVIDIA K-40 accelerators (hereinafter tornado-k40 nodes)
  - 2 × Intel Xeon CPU E5-2697 v3 @ 2.60GHz
  - 64 GB RAM
  - 2 × Nvidia Tesla K40x 12G GDDR

- **288 nodes** of the ultra-high multithreading computing system "Polytechnik - RSK Petastream" (hereinafter mic nodes)
  - 1 × Intel Xeon Phi 5120D @ 1.10GHz
  - 8 GB RAM

All available nodes use a 56Gbps FDR Infiniband network as the interconnect. Additionally, a Lustre parallel file system of about 1 PB is available on all nodes.

**By default, users are granted access to tornado nodes.** Access to other node types is provided upon request.

---

## 2. Access to Resources

Registered users access computing resources via the machine `login1.hpc.spbstu.ru`.

Access is performed using the SSH protocol. Any terminal client supporting the SSH protocol can be used, including:

- **PuTTY** for Windows ([download](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html))
- **OpenSSH** ([openssh.org](http://openssh.org/))

For file copying, the following utilities can be used:

- **WinSCP** for Windows, graphical interface ([winscp.org](http://winscp.org/))
- **pscp/psftp** for Windows, text interface ([download](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html))

---

## 3. Creating SSH Keys

SSH keys are used for authentication to SCC resources. A key pair consists of two files:

- **Private key** — usually password-protected, stored on the user's computer, and never shared.
- **Public key** — stored on the target computer (the one being connected to).

To work with the cluster, you must generate such a key pair.

### 3.1. Creating SSH Keys on Unix Systems

The OpenSSH package is required (installed by default on most distributions). The command below generates a key pair with 4096-bit RSA encryption (`#` denotes the command line prompt).

```bash
# ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
The key fingerprint is:
bf:db:05:bc:0d:c9:2c:b4:8c:2a:c2:70:35:82:05:dd user@host
The key's randomart image is:
+--[RSA 4096]----+
|            .o..|
|            o. E|
|         . . o .|
|        o . + = .|
|         . . S + B|
|        + . . . =|
|       o . . . . o|
|        . . . o|
|         . . o .|
+-----------------+
```

**Important:** After completion, the **private key** is in `/home/user/.ssh/id_rsa`, and the **public key** is in `/home/user/.ssh/id_rsa.pub`. **The public key file must be sent to the SCC registration service.**

### 3.2. Creating SSH Keys on Windows Systems

Example for the PuTTY client.

The `PuTTYgen` utility is required ([download](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)).

**Steps:**

1. Launch PuTTYgen.
2. Set key type to "SSH-2 RSA", size to 2048 bits.
3. Click the "Generate" button (see Figure 1 in original).
4. Move the mouse cursor in the empty area until the progress bar fills completely.
5. Enter a passphrase when prompted (see Figure 2 in original).
6. Click "Save public key" — save as `id_rsa.pub`.
7. Click "Save private key" — save as, e.g., `mykey.ppk`.

> [!NOTE]
> The original document contains Figures 1-3 at this point (screenshots of PuTTYgen interface). They are not available in the provided text.

**The public key file must be sent to the SCC registration service.**

To configure PuTTY to use this key pair:
- Go to `Connection > SSH > Auth` in session settings.
- In the "Private key file for authentication" field, specify the path to the private key file.

---

## 4. Environment Setup

**Environment Modules** are used to manage the environment on SCC "Polytechnichesky" resources. They modify the user's environment.

View available modules:

```bash
$ module avail

--- /usr/share/Modules/modulefiles ---
dot         module-git  module-info modules     null        use.own

--- /opt/basis/modules ---
anys/apdl/16.2                      gromacs/2016/gcc           mic17
anys/apdl/17.0                      gromacs/2016/intel         mic_pmi
anys/apdl/latest                    gromacs/2016/mic           mic_pmi_2017
anys/cfx/16.2                       gromacs/5.1.2/intel
anys/cfx/17.0                       gromacs/5.1.2/mic
anys/cfx/latest                     intel/2016.0.109           mpi/openmpi/2.0.1/gcc/6.2.0
ansys/fluent/16.2                   intel/2016.1.150           numeca/fine101
ansys/fluent/17.0                   intel/2016.3.210(default)  nvidia/cuda-7.5
ansys/fluent/latest                 intel/2017.0.098           parallel/mpi.intel/2017.0.098
compiler/gcc/6.1.0                  intel_license              parallel/mpi.intel/5.1.1.109
compiler/gcc/6.2.0                  launcher/mpiexec           parallel/mpi.intel/5.1.2.150
comsol/52                           launcher/slurm             parallel/mpi.intel/5.1.3.210
espresso/5.4.0                      library/fftw/3.3.4/gcc     parallel/mpi.intel/latest
fds/6.4.0                           library/fftw/3.3.5/gcc     parallel/openmpi/1.10.2/gcc/6.1.0
fftw/3.3.4/gcc                      matlab/2013a               parallel/openmpi/1.10.2/intel/2016.3.210
gcc/5.3.0                           mic                        python/3.5.2
gcc/6.1.0
```

**Available compilers:**
- Intel Compiler 2016.0.109
- Intel Compiler 2016.1.150
- Intel Compiler 2016.3.210
- Intel Compiler 2017.0.098
- GCC 5.3.0
- GCC 6.1.0
- GCC 6.2.0

**Available MPI libraries:**
- Intel MPI 5.0.109
- Intel MPI 5.1.150
- Intel MPI 5.3.210
- Intel MPI 2017.0.098
- OpenMPI 1.10.2
- OpenMPI 2.0.1

**Loading modules:**

```bash
$ module load compiler/gcc/6.2.0
```

**Unloading modules:**

```bash
$ module unload compiler/gcc/6.2.0
```

**Clearing all loaded modules:**

```bash
$ module purge
```

---

## 5. Running Jobs

Resource management on the cluster is performed using the **SLURM** software package.

**Principle:** The user requests resources (CPU cores, memory, etc.) by placing a job in a queue. The system, based on user priority and current queue status, selects when to start the job.

Three queues are currently available for nodes:
- `tornado`
- `tornado-k40`
- `mic`

> [!IMPORTANT]
> Each node can be occupied by only **one job** at any given time. The node is allocated for exclusive use by the job placed on it.

### Batch Script Example

```bash
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH -p tornado
#SBATCH -t 10-00:00:00
#SBATCH -J jobname
#SBATCH -o jobname-%j.out
#SBATCH -e jobname-%j.err

if [ -f /etc/profile.d/modules-basis.sh ]; then
    source /etc/profile.d/modules-basis.sh
fi

module purge
module load mpi/openmpi/2.0.1/gcc/6.2.0

mpiexec /path/to/my/mpi/app
```

### SLURM Directive Explanation

| Directive | Description |
|-----------|-------------|
| `--nodes` | Number of requested nodes |
| `--tasks-per-node` | Number of MPI ranks per node |
| `--cpus-per-task` | Number of OpenMP processes per MPI rank |
| `-p` | Queue name (node type) where the job will be submitted |
| `-t` | Maximum job execution time (must not exceed the queue limit) |
| `-J` | Job name (how it will appear in the queue) |
| `-o` | File for standard output (stdout) |
| `-e` | File for standard error (stderr) |

More detailed descriptions are available in the utility help pages (`man batch`).

### Basic SLURM Commands

| Command | Purpose |
|---------|---------|
| `sbatch run.slurm` | Submit a batch script to the queue |
| `squeue` | View job status |
| `scancel <JOBID>` | Cancel a job |
| `scontrol show jobid <JOBID>` | View detailed job info (includes `StartTime` — estimated start time) |

**Example output of `squeue`:**

```bash
$ squeue
JOBID     PARTITION  NAME      USER   STATE    TIME   NODES
59697     tornado    jobname   user    R       0:01   1
```
