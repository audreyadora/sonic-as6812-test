ifneq ($(KERNELRELEASE),)
obj-m:= marvell_dbmvtx9180_cpld.o \
	marvell_dbmvtx9180_oom.o \
	marvell_dbmvtx9180_leds.o
else
ifeq (,$(KERNEL_SRC))
#$(error KERNEL_SRC is not defined)
KVERSION=3.16.0-8-amd64
KERNEL_DIR   = /usr/src/linux-headers-$(KVERSION)/
KERNELDIR:=$(KERNEL_DIR)
else
KERNELDIR:=$(KERNEL_SRC)
endif
PWD:=$(shell pwd)
default:
	$(MAKE) -C $(KERNELDIR)  M=$(PWD) modules
clean:
	rm -rf  *.o *.mod.o *.mod.o *.ko .*cmd *.mod.c *.mod .tmp_versions Module.markers Module.symvers modules.order
endif
