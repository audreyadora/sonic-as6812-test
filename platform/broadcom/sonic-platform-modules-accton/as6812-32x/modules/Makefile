ifneq ($(KERNELRELEASE),)
obj-m:= x86-64-accton-as6812-32x-cpld.o \
        x86-64-accton-as6812-32x-fan.o \
        x86-64-accton-as6812-32x-leds.o \
        x86-64-accton-as6812-32x-psu.o 
         
else
ifeq (,$(KERNEL_SRC))
$(error KERNEL_SRC is not defined)
else
KERNELDIR:=$(KERNEL_SRC)
endif
PWD:=$(shell pwd)
default:
	$(MAKE) -C $(KERNELDIR)  M=$(PWD) modules
clean:
	rm -rf *.o *.mod.o *.mod.o *.ko .*cmd .tmp_versions Module.markers Module.symvers modules.order
endif
