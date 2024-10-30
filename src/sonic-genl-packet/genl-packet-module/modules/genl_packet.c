#include <linux/module.h>
#include <net/genetlink.h>

#define GENL_PACKET_MCGRP_NAME "packets"
#define GENL_PACKET_NAME "genl_packet"
#define GENL_PACKET_VERSION 1
#define GENL_PACKET_ATTR_MAX 4

/* multicast groups */
enum genl_packet_multicast_groups {
  GENL_PACKET_MCGRP_PACKET,
};

static const struct genl_multicast_group genl_packet_mcgrps[] = {
    [GENL_PACKET_MCGRP_PACKET] = {.name = GENL_PACKET_MCGRP_NAME},
};

static struct genl_family genl_packet_family = {
    .name = GENL_PACKET_NAME,
    .version = GENL_PACKET_VERSION,
    .maxattr = GENL_PACKET_ATTR_MAX,
    .netnsok = true,
    .module = THIS_MODULE,
    .mcgrps = genl_packet_mcgrps,
    .n_mcgrps = ARRAY_SIZE(genl_packet_mcgrps),
};


static int __init genl_packet_module_init(void) {
  return genl_register_family(&genl_packet_family);
}

static void __exit genl_packet_module_exit(void) {
  genl_unregister_family(&genl_packet_family);
}

module_init(genl_packet_module_init);
module_exit(genl_packet_module_exit);

MODULE_AUTHOR("ONF");
MODULE_DESCRIPTION("temporary netlink registration for genl_packet");
MODULE_LICENSE("GPL v2");
