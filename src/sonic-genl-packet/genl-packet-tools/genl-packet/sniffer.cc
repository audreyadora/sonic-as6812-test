#include "libgenl-packet/genl-packet/receive_genetlink.h"
#include <iostream>
#include "PcapFileDevice.h"
#include "PayloadLayer.h"
#include "Packet.h"
#include "SystemUtils.h"
#include <gflags/gflags.h>
#include <sys/time.h>
#include <glog/logging.h>

//flags
DEFINE_string(output_file, "out.pcapng", "Choose output. Leave blank for standard out or provide a filename");
DEFINE_bool(append, false, "Append to the output file. Default is overwrite");
DEFINE_bool(verbose, false, "Print the hex packet, packet comment and the payload to standard out");

//Conversion from a binary string to the Hex representation.
std::string StringToHex(const std::string& str) {
  static const char* const characters = "0123456789ABCDEF";
  std::string hex_str;
  const size_t size = str.size();
  hex_str.reserve(2 * size);
  for (size_t i = 0; i < size; ++i) {
    const unsigned char c = str[i];
    hex_str.push_back(characters[c >> 4]);
    hex_str.push_back(characters[c & 0xF]);
  }
  return hex_str;
}

//custom callback exposed function
int customCallbackRecieve(packet_metadata::ReceiveCallbackFunction callback) {
  auto thread = packet_metadata::StartReceive(callback);
  thread.join();
  return 0;
}

int main(int argc, char* argv[]) {

  //flag processing commands
  gflags::ParseCommandLineFlags(&argc, &argv, true);
  google::InitGoogleLogging(argv[0]);

  pcpp::PcapNgFileWriterDevice writer(FLAGS_output_file);
  if (FLAGS_output_file != "-") {
  //append or overwrite the existing file
    if (!FLAGS_append) {
      writer.open();
      writer.close();
    }
  }
  //standard callback
  auto callback = [&writer](const std::string &source_port_name,
                     const std::string &target_port_name,
                     //timestamp, etc. other metadate can be added down later
                     const std::string &payload) -> void {
    const uint8_t* data = reinterpret_cast<const uint8_t*>(payload.c_str());
    pcpp::PayloadLayer newPayloadLayer(data, payload.length(), true);
    //creating the comment string for the packet
    std::string com;
    com.append("Ingress Port: ");
    com.append(source_port_name);
    com.append(". Outgress Port: ");
    com.append(target_port_name);
    pcpp::Packet newPacket(100);
    newPacket.addLayer(&newPayloadLayer);
    newPacket.computeCalculateFields();
    if (FLAGS_output_file != "-") {
      writer.open(true);
      writer.writePacket(*(newPacket.getRawPacket()), com);
      writer.close();
    }
    if (FLAGS_output_file == "-") {
      std::cout << StringToHex(payload) << std::endl;
    }
    if (FLAGS_verbose) {
      std::cout << "Packet start" << std::endl;
      std::cout << "Hex packet: " << StringToHex(payload) << std::endl;
      std::cout << "Payload: " << payload << std::endl;
      std::cout << "Packet comment: " << com << std::endl;
      std::cout << "Packet end" << std::endl;
    }
  };
  auto thread = packet_metadata::StartReceive(callback);
  thread.join();
  return 0;
}
