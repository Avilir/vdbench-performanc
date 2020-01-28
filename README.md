# vdbench-performanc
Container and Scripts for running vdbench

[VDbench](https://www.oracle.com/downloads/server-storage/vdbench-downloads.html) -- is a tool used for benchmarking
and stress-testing I/O subsystems. We generally refer to this type of workload as a "microbenchmark"
because it is used in a targeted way to determine the bottlenecks and limits of a system.
this tool written and maintain by oracle and it is highly used my the industry.

VDbench can be run as a singel-host or multi-host test and has a native mechanism to run multiple servers concurrently
against a data store. This Container used to build the basic container that can run the benchmark against up to 10 volumes, connecting as block or file devices.


Vdbench can be downloaded from [Oracle site](http://www.oracle.com/technetwork/server-storage/vdbench-downloads-1901681.html)
It is free of charge, but you must login to download it, and this is why i did not put it here.

The Current build of vdbench, which used in this repository is : 5.04.07

For building this container you need to do :

    * Clone this repository
    * Download the vdbench from the oracle site into the repo. directory
    * Modify the build.sh script (if needed)
       - changing repo name / container tool (podman / docker)
    * running the build.sh script and pass to it the tag name for the build.
