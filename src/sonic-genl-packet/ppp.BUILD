cc_library(
    name = "common",
    srcs = glob(["Common++/src/*.cpp"], allow_empty=False),
    hdrs = glob(["Common++/header/*.h"]),
    strip_include_prefix = "Common++/header",
    visibility = ["//visibility:public"],
    deps = [
        ":endian_portable",
    ],
    defines = ["LINUX"],
)

cc_library(
    name = "packet",
    srcs = glob(["Packet++/src/*.cpp"], allow_empty=False),
    hdrs = glob(["Packet++/header/*.h"]),
    strip_include_prefix = "Packet++/header",
    visibility = ["//visibility:public"],
    deps = [
        ":common",
        ":endian_portable",
        ":hash_lib",
    ],
)

cc_library(
    name = "pcap",
    srcs = glob(["Pcap++/src/*.cpp"], allow_empty=False),
    hdrs = glob(["Pcap++/header/*.h"]),
    strip_include_prefix = "Pcap++/header",
    visibility = ["//visibility:public"],
    deps = [
        ":packet",
        ":light_pcapng"
    ],
    copts = ["-I", "/usr/include/pcap/"],
    linkopts = ["-lpcap"],
)

cc_library(
    name = "endian_portable",
    hdrs = ["3rdParty/EndianPortable/include/EndianPortable.h"],
    strip_include_prefix = "3rdParty/EndianPortable/include", 
)

cc_library(
    name = "light_pcapng",
    hdrs = glob(["3rdParty/LightPcapNg/LightPcapNg/include/*.h"]),
    srcs = glob(["3rdParty/LightPcapNg/LightPcapNg/src/*.c"]),
    strip_include_prefix = "3rdParty/LightPcapNg/LightPcapNg/include", 
)

cc_library(
    name = "hash_lib",
    hdrs = ["3rdParty/hash-library/md5.h"],
    srcs = ["3rdParty/hash-library/md5.cpp"],
    strip_include_prefix = "3rdParty/hash-library",
    deps = [":endian_portable",]
)