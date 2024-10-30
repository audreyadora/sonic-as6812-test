#include <linux/netlink.h>
#include <net/if.h>
#include <netlink/genl/ctrl.h>
#include <netlink/genl/family.h>
#include <netlink/genl/genl.h>
#include "uapi/linux/genl-packet.h"
#include <iostream>

struct nlsock_holder {
    struct nl_sock* nlsock;
    int family_id;
    int group_id;
};

// Custom Deleter used for the nlsock_holder struct. 
// We use it because it lets us delete the innerlying nlsock pointer within the smart pointer.
struct Deleter {
    void operator()(nlsock_holder* nlholder) {
        std::cout << "delete stuff" << std::endl;
        if (nlholder != nullptr) {
            nl_socket_free(nlholder->nlsock);
        }
    }
};

std::unique_ptr<struct nlsock_holder, Deleter> PrepareNetlinkSocket(const char family_name[]) {
    struct nl_sock* nlsock;
    nlsock = nl_socket_alloc();
    if (nlsock == nullptr) {
        return nullptr;
    }
    // Disable automatic request of ACK for every message.
    nl_socket_disable_auto_ack(nlsock);
    // Connect to generic netlink.
    int error = genl_connect(nlsock);
    if (error < 0) {
        nl_socket_free(nlsock);
        return nullptr;
    }
    // Resolve the generic netlink family id.
    int family_id = genl_ctrl_resolve(nlsock, family_name);
    if (family_id < 0) {
        nl_socket_free(nlsock);
        return nullptr;
    }
    std::unique_ptr<struct nlsock_holder, Deleter> nl_holder = 
        std::unique_ptr<struct nlsock_holder, Deleter>(new nlsock_holder, Deleter());
    nl_holder->nlsock = nlsock;
    nl_holder->family_id = family_id;
    return nl_holder;
}

std::unique_ptr<struct nlsock_holder, Deleter> PrepareNetlinkSocketSender(const char family_name[], const char group_name[]) {
    std::unique_ptr<struct nlsock_holder, Deleter> nl_holder = PrepareNetlinkSocket(family_name);
    if (nl_holder == nullptr) {
        return nullptr;
    }
    int group_id = genl_ctrl_resolve_grp(nl_holder->nlsock, family_name,
                                       group_name);
    if (group_id < 0) {
        std::cout << "Error: Group id: " << group_id << std::endl;
        nl_socket_free(nl_holder->nlsock);
        return nullptr;
    }
    nl_holder->group_id = group_id;
    nl_socket_set_peer_groups(nl_holder->nlsock, (1 << (group_id - 1)));
    return nl_holder;
}

std::unique_ptr<struct nlsock_holder, Deleter> PrepareNetlinkSocketReceiver(const char family_name[], const char group_name[]) {
    std::unique_ptr<struct nlsock_holder, Deleter> nl_holder = PrepareNetlinkSocket(family_name);
    if (nl_holder == nullptr) {
        return nullptr;
    }
    int group_id = genl_ctrl_resolve_grp(nl_holder->nlsock, family_name,
                                       group_name);
    if (group_id < 0) {
        nl_socket_free(nl_holder->nlsock);
        return nullptr;
    }
    nl_holder->group_id = group_id;
    int error = nl_socket_add_membership(nl_holder->nlsock, group_id);
    if (error < 0) {
        nl_socket_free(nl_holder->nlsock);
        return nullptr;
    }
    return nl_holder;
}