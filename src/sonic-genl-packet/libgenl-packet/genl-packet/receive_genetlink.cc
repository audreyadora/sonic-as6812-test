// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <linux/netlink.h>
#include <net/if.h>
#include <netlink/genl/ctrl.h>
#include <netlink/genl/family.h>
#include <netlink/genl/genl.h>
#include <sstream>
#include <errno.h>
#include <system_error>
#include <stdexcept>
#include <glog/logging.h>
#include <memory>
#include "uapi/linux/genl-packet.h"
#include "prepare_netlink.h"
#include "receive_genetlink.h"

namespace packet_metadata {

    // A structure to hold parameters necessary for the Netlink callback function.
    struct NetlinkCallbackArgs {
        NetlinkCallbackArgs(struct nla_policy* const genl_attr_policy,
        ReceiveCallbackFunction callback_function)
        : genl_attr_policy_(genl_attr_policy), callback_function_(callback_function) {}
        ~NetlinkCallbackArgs() {
            if (genl_attr_policy_) {
                 delete genl_attr_policy_;
            }
        }
        struct nla_policy* const genl_attr_policy_;
        const ReceiveCallbackFunction callback_function_;
    };

namespace {

    // Convert ifindex to the corresponding interface name.
    std::string GetIfname(int16_t ifindex) {
        if (ifindex < 0){
            std::string err = "Index must be greater than 0, index: ";
            LOG(ERROR) << err + std::to_string(ifindex);
            throw std::invalid_argument(err + std::to_string(ifindex));
        }
        if (ifindex == 0) return std::string("");
        char ifname[IF_NAMESIZE] = {0};
        auto retval = if_indextoname(ifindex,ifname);
        if (retval == nullptr){
            std::ostringstream ss;
            ss << "Failed to convert ifindex: " << ifindex << "to ifname, errno: " << errno;
            throw std::invalid_argument(ss.str());
        }
        return std::string(ifname);
    }


    static void ReceiveThread(std::unique_ptr<struct nlsock_holder, Deleter> nlholder, struct nl_cb* cb) {
        LOG(INFO) << "Successfully created Netlink Receive thread";
        // Blocking call to receive packets on the Netlink socket.
        while (true) {
            int error = nl_recvmsgs(nlholder->nlsock, cb);
            // Packet processing happens in the ProcessReceiveMessageCallback()
             // function.
            if (error < 0) {
                LOG(WARNING) << std::string("Failed in receive message callback from netlink socket,\
	            error: %d", error);
            }
        }
        // Never expect to be here.
    }

}  // namespace

// Process a receive message to retrieve the netlink attribute values.
// Function is called from the netlink lib
// Should always return NL_OK
int ProcessReceiveMessageCallback(struct nl_msg* msg, void* arg) {
  auto* const nl_cb_args = reinterpret_cast<NetlinkCallbackArgs*>(arg);
  if (nl_cb_args == nullptr) {
    LOG(ERROR) << "NetlinkCallbackArgs is inexplicably null";
    return NL_OK;
  }

  struct nlattr* attr[GENL_PACKET_ATTR_MAX] = {0};
  // Parse the incoming message per the defined netlink attributes.
  int error = genlmsg_parse(nlmsg_hdr(msg), /*hdrlen=*/0, attr, GENL_PACKET_ATTR_MAX,
                            nl_cb_args->genl_attr_policy_);
  if (error < 0) {
    LOG(ERROR) << std::string("Failed to parse packet erroo: %d",error);
    return NL_OK;
  }

  std::string source_port_name, target_port_name;
  std::string packet;
  for (int i = 0; i < GENL_PACKET_ATTR_MAX; i++) {
    if (attr[i]) {
      switch (i) {
        case GENL_PACKET_ATTR_IIFINDEX : {
          /*G3_WA*/
          auto port = nla_get_u16(attr[i]);
          const auto name = GetIfname(port);
          source_port_name = name;
          break;
        }
        case GENL_PACKET_ATTR_OIFINDEX: {
          auto port = nla_get_u16(attr[i]);
          const auto name = GetIfname(port);
          target_port_name = name;
          break;
        }
        case GENL_PACKET_ATTR_CONTEXT: {
          break;
        }
        case GENL_PACKET_ATTR_DATA: {
          packet = std::string(static_cast<const char*>(nla_data(attr[i])),
                               static_cast<size_t>(nla_len(attr[i])));
          break;
        }
        default: {
          LOG(WARNING) << std::string("Unexpected Netlink attribute %s in the packet metadata",i);
          break;
        }
      }
    }
  }

  if (packet.empty()) {
    LOG(ERROR) << "Empty payload skipping";
  } else if (source_port_name.empty()) {
    LOG(ERROR) << "No source port, skipping this packet";
  } else { 
      (nl_cb_args->callback_function_)(source_port_name,target_port_name, packet);
  }
  // Always return OK to move on to the next packet.
  return NL_OK;
}
//change to include callback within appl_callback, one netlink aware one netlink unaware
// genl_attr_policy should be provided by the user
//fixed
std::thread StartReceiveCustom( ReceiveCallbackFunction callback_function, nl_recvmsg_msg_cb_t  appl_callback_function) {
  struct nl_cb* cb = nullptr;

  //on failure will propogate execption
  std::unique_ptr<struct nlsock_holder, Deleter> nl_holder = PrepareNetlinkSocketReceiver(GENL_PACKET_NAME, GENL_PACKET_MCGRP_NAME);
    if (nl_holder == nullptr) {
      LOG(ERROR) << "Could not create an nlsock";
    }

  // Set the receive policies for all netlink packet attribures.
  auto* genl_attr_policy = new struct nla_policy[__GENL_PACKET_ATTR_MAX];
  memset(genl_attr_policy, 0, sizeof(struct nla_policy) * __GENL_PACKET_ATTR_MAX);
  genl_attr_policy[GENL_PACKET_ATTR_IIFINDEX].type = NLA_U16;
  genl_attr_policy[GENL_PACKET_ATTR_OIFINDEX].type = NLA_U16;
  genl_attr_policy[GENL_PACKET_ATTR_CONTEXT].type = NLA_U32;
  genl_attr_policy[GENL_PACKET_ATTR_DATA].type = NLA_UNSPEC;

  // Register the callback function for receive packet processing.
  cb = nl_cb_alloc(NL_CB_DEFAULT);
  auto* nl_cb_args = new NetlinkCallbackArgs(genl_attr_policy, callback_function);

  nl_cb_set(cb, NL_CB_VALID, NL_CB_CUSTOM, appl_callback_function, reinterpret_cast<void*>(nl_cb_args));
  // Create Receive thread to receive packets from the socket.
  std::thread receive_thread(ReceiveThread, std::move(nl_holder), cb);
  return receive_thread;
}
    std::thread StartReceive(packet_metadata::ReceiveCallbackFunction 
    callback_function) {
        return packet_metadata::StartReceiveCustom(callback_function, 
        packet_metadata::ProcessReceiveMessageCallback);
    }
}  // namespace packet_metadata
