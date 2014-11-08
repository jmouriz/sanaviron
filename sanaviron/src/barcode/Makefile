#-m32 and -melf_i386 for compile the 32-bit libraries on x86_64 OS
CFLAGS = -g -O2 -Wall -DHAVE_UNISTD_H=1 -DHAVE_STRCASECMP=1 -DNO_LIBPAPER -fPIC
TARGET = barcode
CC = gcc
SHARED = $(TARGET).so
#SHARED = $(TARGET).dll
HEADER = $(TARGET).h

INSTALL = /usr/bin/install -c

DSTDIR = ../../objects/barcode

LIBOBJECTS = \
   barcode.o \
   interface.o \
   postnet.o \
   iec16022ecc200.o \
   reedsol.o \
   library.o \
   ean.o \
   code128.o \
   code39.o \
   code93.o \
   i25.o \
   msi.o \
   plessey.o \
   codabar.o \
   ps.o \
   pcl.o \
   bitstream.o \
   mask.o \
   mmask.o \
   mqrspec.o \
   qrencode.o \
   qrinput.o \
   qrspec.o \
   rscode.o \
   split.o

ALLSOURCES = $(LIBOBJECTS:.o=.c)

RM = rm

all: $(SHARED)

$(SHARED): $(LIBOBJECTS)
	$(CC) -shared -o $(SHARED) $(LIBOBJECTS)

install:
	$(INSTALL) -c -m 0644 $(SHARED) $(DSTDIR) 

uninstall:
	$(RM) -f $(DSTDIR)/$(SHARED)

# Make clean keeps the compiled documents
clean:
	-$(RM) -f *.o */*.o *~ */*~ core

# Make purge remove the compiled documents
purge: clean
	-$(RM) -f */*.o *~ */*~ core $(SHARED)
