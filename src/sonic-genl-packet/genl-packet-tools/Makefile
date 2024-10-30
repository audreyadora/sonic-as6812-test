PREFIX = /usr

genl-packet:
	bazel build genl-packet:sniffer
	bazel build genl-packet:generator

install: 
	install -D ../bazel-bin/genl-packet-tools/genl-packet/sniffer $(DESTDIR)$(PREFIX)/bin/genl-packet-sniffer
	install -D ../bazel-bin/genl-packet-tools/genl-packet/generator $(DESTDIR)$(PREFIX)/bin/genl-packet-generator 

clean:
	bazel clean --expunge

uninstall:
	-rm  $(DESTDIR)$(PREFIX)/bin/genl-packet-sniffer
	-rm  $(DESTDIR)$(PREFIX)/bin/genl-packet-generator

.PHONY: install clean uninstall genl-packet
