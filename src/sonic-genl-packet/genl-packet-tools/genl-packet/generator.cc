#include <linux/netlink.h>
#include <net/if.h>
#include <netlink/genl/ctrl.h>
#include <netlink/genl/family.h>
#include <netlink/genl/genl.h>
#include <sstream>
#include <bitset>
#include <string>
#include <bits/stdc++.h>
#include <gflags/gflags.h>
#include <iostream>
#include "stdlib.h"
#include "SystemUtils.h"
#include "Packet.h"
#include "PayloadLayer.h"
#include "PcapFileDevice.h"
#include "libgenl-packet/genl-packet/prepare_netlink.h"
#include "libgenl-packet/genl-packet/uapi/linux/genl-packet.h"

using namespace std;

// Flags definition.
DEFINE_string(test_packet, "8cea1b17640c0007434b7f5008004500001c0001000040110a19c0a80201ac1001fe0000000000088f26", "Input a test packet. If none given a default test packet is used.");
DEFINE_string(test_input_file, "", "A .pcapng file from which the packets will be parsed and sent via genetlink. If none provided one provided or sample packet will be sent.");

// Sending a packet.
void genl_send_pkt(const char *pkt, uint32_t size,
                   int in_ifindex, int out_ifindex, unsigned int context, 
                   std::unique_ptr<struct nlsock_holder, Deleter> &nl_holder)
{
    int err = 0;
    struct nl_msg *msg = nlmsg_alloc();
    genlmsg_put(msg, NL_AUTO_PORT, NL_AUTO_SEQ, nl_holder->family_id,
                0, 0, 0, 1);
    NLA_PUT_S16(msg, GENL_PACKET_ATTR_IIFINDEX, in_ifindex);
    NLA_PUT_S16(msg, GENL_PACKET_ATTR_OIFINDEX, out_ifindex);
    NLA_PUT_U32(msg, GENL_PACKET_ATTR_CONTEXT, context);
    NLA_PUT(msg, GENL_PACKET_ATTR_DATA, size, pkt);
    if ((err = nl_send(nl_holder->nlsock, msg)) < 0)
    {
        std::cout << "My Error: " << nl_geterror(err) << std::endl;
    }
    std::cout << "Byte sent: " << err << std::endl;
    nlmsg_free(msg);
    return;
nla_put_failure:
    std::cout << "My Error: put error"  << std::endl;
    nlmsg_free(msg);
    return;
}

// Conversion between a hex string and a binary char string.
string hexToChars(string hex)
{
    string chars = "";
    for (size_t i = 0; i < hex.length(); i += 2)
    {
        string part = hex.substr(i, 2);
        char ch = stoul(part, nullptr, 16);
        chars += ch;
    }
    return chars;
}

int main(int argc, char* argv[]) {

    gflags::ParseCommandLineFlags(&argc, &argv, true); 

    // Input pcap file and send packets or provide packet string.
    std::unique_ptr<struct nlsock_holder, Deleter> nl_holder = PrepareNetlinkSocketSender((char*)GENL_PACKET_NAME, (char*)GENL_PACKET_MCGRP_NAME);
    if (nl_holder == nullptr) {
      return 1;
    }

    if (FLAGS_test_input_file != "") {
      pcpp::IFileReaderDevice* reader = pcpp::IFileReaderDevice::getReader(FLAGS_test_input_file);
      
      if (reader == NULL) {
        std::cerr << "Non existent file or cannot determine reader for file type" << std::endl;
        return 1;
      }

      if (!reader->open()) {
        std::cerr << "Cannot open the file for reading" << std::endl;
        return 1;
      }

      pcpp::RawPacket rawPacket;
      while (reader->getNextPacket(rawPacket)) {
        pcpp::Packet parsedPacket(&rawPacket);
        pcpp::PayloadLayer* paylLayer = parsedPacket.getLayerOfType<pcpp::PayloadLayer>();
        uint8_t* pkt_data = paylLayer->getPayload();
        int size = paylLayer->getPayloadLen();
        genl_send_pkt((char *) pkt_data, size, 2, 2, 3, nl_holder);
      }
      reader->close();
    } else {
      string pkt = hexToChars(FLAGS_test_packet);
      int size = pkt.length();
      genl_send_pkt(pkt.c_str(), size, 2, 2, 3, nl_holder);
    }
    return 0;
}
