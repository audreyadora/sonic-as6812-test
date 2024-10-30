# sonic-genl-packet
**This is a work in progress, frequent changes are likely while this message appears**
## Overview
Generic Netlink provides a means of passing packets with additional developer defined metadata within a *nix system via a multicast-like mechanism.  The generic device needs to be created by a privleged user but reading and writing packets are userspace accessible.


This repository contains the source code for two applications which can be used for tracking/debugging genetlink traffic. 
The first [sniffer] can be used for listening to traffic, as well as recording the traffic into a file or displaying to standard out. The resulting pcapng file 
can then be viewed using Wireshark.
The second [generator] can be used to send an example packet or packets from a pcap/pcapng file through genetlink. 

The first version of the library separates the receive_genetlink functionality into two files. First one is the main receive_genetlink code, which contains the full functionality. Second one is receive_genetlink_custom which facilitates the use of the library without the need to have a libnl compilation option as the netlink arguments are hidden for the sake of current use cases.

### Dependencies
The dependencies are four different libnl packages. They can be installed with install_deps.sh

### Building

Both [sniffer] and [generator] use bazel as their build system, so you can either compile locally using 
```
bazel build genl-packet:sniffer
bazel build genl-packet:generator
```
or using sonic-buildimage.

### Sniffer [sniffer]

If compiled locally the binary can be found in bazel-bin/genl-packet/sniffer. If compiled using sonic-buildimage and the package installed you can call the binary using genl-packet. For the following commands we will call it [binary].
Whichever way you choose the following commands will help you in listening to genetlink traffic:
```
[binary]
```
This will simply launch a listener and record all the traffic into out.pcapng

```
[binary] -a
```
Providing the -a flag will either append to out.pcapng or a different file if provided. 

```
[binary] -o=-
```
This will print the hex representation of the received packets to standard out.

```
[binary] -o=hello.pcapng
```
By providing a filename you can write the genetlink packets into a given file. In this example it will be hello.pcapng

```
[binary] -verbose
```
This flag will print out verbose information about the packets received including metadata and packet contents. 

### Traffic generator [generator]

If compiled locally the binary can be found in bazel-bin/genl-packet/generator. If compiled using sonic-buildimage and the package installed you can call the binary using genl-packet-test. For the following commands we will call it [binary_test].
You can use the following commands to generate some netlink traffic and test it:
```
sudo [binary_test]
```
This will simply send a sample packet once through genetlink.

```
sudo [binary_test] -inputfile=hello.pcapng
```
Providing an input file will read packets from the file and send them via genetlink.

```
sudo [binary_test] -packet=AABBCCDD
```
Providing an input packet will send that packet once via genetlink. It is reccomended that you provide a valid packet.

