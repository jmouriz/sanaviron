#-m32 and -melf_i386 for compile the 32-bit librarieson x86_64 OS
CFLAGS = -g -O2 -Wall -DHAVE_UNISTD_H=1 -DHAVE_STRCASECMP=1 -DNO_LIBPAPER -fPIC -m32
LDFLAGS += -melf_i386
TARGET = wide-string
CC = gcc
SHARED = $(TARGET).so
#SHARED = $(TARGET).dll
HEADER = $(TARGET).h

INSTALL = /usr/bin/install -c

DSTDIR = ../../objects/wide-string

LIBOBJECTS = wide-string.o

ALLSOURCES = $(LIBOBJECTS:.o=.c)

RM = rm

all: $(SHARED)

$(SHARED): $(LIBOBJECTS)
	$(CC) -m32 -shared -o $(SHARED) $(LIBOBJECTS)

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
