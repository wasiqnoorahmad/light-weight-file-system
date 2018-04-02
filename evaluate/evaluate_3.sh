#!/bin/bash

cd $HOME/nfs/
max=13
for i in `seq 9 $max`
do
    BYTES_SIZE=$(echo "2^$i"|bc)
    rm -rf db/db3
    python task3/setdb.py $BYTES_SIZE

    # Mount FS of task{1,2,3} with KB as 2^{9,10,11,12,13}
    ./mount.sh task3 $BYTES_SIZE

    for j in {1..3}
    do
        # dd Command to measure read time throughput
        dd if=mountpoint/4nb bs=$BYTES_SIZE count=1 oflag=dsync 2>> evaluate/output_task3.txt
        # dd Command to measure write time throughput
        dd if=mountpoint/4nb of=mountpoint/vaf bs=$BYTES_SIZE count=1 oflag=dsync 2>> evaluate/output_task3.txt
    done
    for j in {1..3}
    do
        # dd Command to measure read time latency
        dd if=mountpoint/4nb bs=$BYTES_SIZE count=1000 oflag=dsync 2>>evaluate/output_task3.txt
        # dd Command to measure write time latency
        dd if=mountpoint/4nb of=mountpoint/vaf bs=$BYTES_SIZE count=1000 oflag=dsync 2>> evaluate/output_task3.txt
    done
    sleep 2
    ./unmount.sh
done
