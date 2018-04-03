# FUSE Filesystem #

Disclaimer: Empty directories are not useless in this project folder. You will find them of usefull once you follow this README
file. So, please do not delete them.

## About ##
This project implements a simple Fuse Based FileSystem using LevelDB and Python 2.7. Aim of this project is implement all the features that a concrete filesystem
should support. It uses the simple idea to storing content, meta data, filenames and all filesystem relevant stuff into LevelDB and use FUSE APIs to invoke desired
features of a filesystem.

It has 3 parts mainly. Starting from reading and writing from direct LevelDB followed by implementing INodes and lastly all other file operations like rename,
 delete, copy etc.

### Prerequisties ###
* Python 2.7
* FUSE
* Python-Fuse
* Plyvel (LevelDB)

## Mounting ##
To mount and start using this filesystem, first we need to dump dummy data into LevelDB to see some results in our filesystem.
Every task has *setdb.py* script that dumps dummy data into the Leveldb. (All the databases are created in *db* folder). 
This script takes block size as command line argument. So, you can execute this script as shown in the example below:
**sudo python setdb.py 512**

Once you have filled the LevelDB, you are ready to mount the filesystem in *mountpoint* directory. This can be done by simply
executing the *mount.sh* script. Usage is as follow:

**sudo ./mount.sh task<1,2,3> <block size>**
***example: ./mount.sh task1 512 ***

It will mount the filesystem in *mountpoint* directory. Open this directory and play with files (as per the question requirement).

## Unmounting ##
To unmount the filesystem just execute the unmount script as follow:
**sudo ./unmount.sh**

  - - - -

## Evaluation ##
To evaluate the perofrmance of the filesystem. Go into the evaluation directory and execute the shell script
revelant to the part you are going to evaluate. For example, to evaluate Part 1, simple execute *evaluate_1.sh* with command:

**sudo ./evaluate_1.sh**

This script measures the throughput and latency of the filesystem using *dd* utility. An example command to measure throughput is:

**dd if=mountpoint/<some file name> bs=<block size> count=1 oflag=dsync 2>> evaluate/<output file name>**

This command produces the following result:

**0+1 records in**
**0+1 records out**
**452 bytes copied, 0.000720203 s, 628 kB/s**

Output shows that 628 kB/s is the latency.

Similarly, latency can also be calculated using *dd* with following command:

**dd if=mountpoint/<some file name> bs=<block size> count=1000 oflag=dsync 2>> evaluate/<output file name>**

Following results are produced:

**0+1 records in**
**0+1 records out**
**452 bytes copied, 0.000884651 s, 511 kB/s**

Indicating that 0.000884651 is the latency.
