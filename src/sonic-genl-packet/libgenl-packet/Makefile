PREFIX = /usr

libgenl-packet:
	bazel build genl-packet:genl_packet

install: libgenl-packet
	install -D genl-packet/receive_genetlink.h $(DESTDIR)$(PREFIX)/include/receive_genetlink.h
	install -D genl-packet/uapi/linux/genl-packet.h $(DESTDIR)$(PREFIX)/include/uapi/linux/genl-packet.h
	install -D ../bazel-bin/libgenl-packet/genl-packet/libgenl_packet.so $(DESTDIR)$(PREFIX)/lib/libgenl_packet.so
	install -D ../bazel-bin/libgenl-packet/genl-packet/libgenl_packet.a $(DESTDIR)$(PREFIX)/lib/libgenl_packet.a
clean:
	bazel clean --expunge

uninstall:
	-rm -f $(DESTDIR)$(PREFIX)/bin/genl-packet

.PHONY: install clean uninstall genl-packet
