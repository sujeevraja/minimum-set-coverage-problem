# Copyright (C) 2006 International Business Machines and others.
# All Rights Reserved.
# This file is distributed under the Eclipse Public License.

# $Id: Makefile.in 1898 2013-04-09 18:06:04Z stefan $

##########################################################################
#    You can modify this example makefile to fit for your own program.   #
#    Usually, you only need to change the five CHANGEME entries below.   #
##########################################################################

# uncomment the following 2 lines and change CBCDIR to point to the Cbc folder to enable functions
# that use Cbc to solve MIPs.
USE_CBC = TRUE
CBCDIR = $(HOME)/coin/Cbc-2.9.8

BOOSTDIR = $(HOME)/boost_1_63_0

# To compile other examples, either changed the following line, or
# add the argument DRIVER=problem_name to make
# CBCDIR = $(HOME)/coin/Cbc-2.9.8
DRIVER = main

# CHANGEME: This should be the name of your executable
EXE = $(DRIVER).out

# CHANGEME: Directory to the sources for the (example) problem definition
# files
SRCDIR = ./src

# CHANGEME: Here is the name of all object files corresponding to the source
#           code that you wrote in order to define the problem statement
OBJS =  $(SRCDIR)/$(DRIVER).o

# extra object files that are required by some examples (we just link them into each one)
EXTRAOBJS = \
	$(SRCDIR)/Controller.o \
	$(SRCDIR)/ProblemInstance.o \
	$(SRCDIR)/Solver.o \
	$(SRCDIR)/Utility.o

# CHANGEME: Additional libraries
# e.g., for driver2, put -lOsiCbc here
ADDLIBS =

# CHANGEME: Additional flags for compilation (e.g., include flags)
ADDINCFLAGS = -std=c++11 -MMD -MP -isystem$(BOOSTDIR)

##########################################################################
#  Usually, you don't have to change anything below.  Note that if you   #
#  change certain compiler options, you might have to recompile the      #
#  package.                                                              #
##########################################################################

# C++ Compiler command
CXX = g++

# C++ Compiler options
CXXFLAGS = -O3 -pipe -DNDEBUG -pedantic-errors -Wparentheses -Wreturn-type -Wcast-qual -Wall -Wpointer-arith -Wwrite-strings -Wconversion -Wno-unknown-pragmas -Wno-long-long   -DCBC_BUILD

# C Compiler options
CFLAGS = -O3 -pipe -DNDEBUG -pedantic-errors -Wimplicit -Wparentheses -Wsequence-point -Wreturn-type -Wcast-qual -Wall -Wno-unknown-pragmas -Wno-long-long   -DCBC_BUILD

# additional C++ Compiler options for linking
CXXLINKFLAGS =

INCL = -I$(SRCDIR) $(ADDINCFLAGS)

# Linker flags
LIBS =

ifeq ($(USE_CBC), TRUE)
CXXFLAGS +=  -DUSE_CBC
CFLAGS +=  -DUSE_CBC
CXXLINKFLAGS +=  -Wl,-rpath -Wl,$(CBCDIR)/lib
INCL +=  -isystem$(CBCDIR)/include/coin
LIBS += \
	-L$(CBCDIR)/lib \
	-lCbcSolver \
	-lCbc \
	-lOsiCbc \
	-lOsiClp \
	-lClpSolver \
	-lClp \
	-lOsi \
	-lCoinUtils \
	-lm \
	-lCgl
endif

# The following is necessary under cygwin, if native compilers are used
CYGPATH_W = echo

# Here we list all possible generated objects or executables to delete them
CLEANFILES = \
	$(OBJS) \
	$(OBJS:.o=.d) \
	$(EXTRAOBJS) \
	$(EXTRAOBJS:.o=.d) \
	$(EXE)

all: $(EXE)

-include $(OBJS:.o=.d)
-include $(EXTRAOBJS:.o=.d)

.SUFFIXES: .cpp .c .o .obj

$(EXE): $(OBJS) $(EXTRAOBJS)
	bla=;\
	for file in $(OBJS) $(EXTRAOBJS); do bla="$$bla `$(CYGPATH_W) $$file`"; done; \
	$(CXX) $(CXXLINKFLAGS) $(CXXFLAGS) -o $@ $$bla $(LIBS) $(ADDLIBS)

clean:
	rm -rf $(CLEANFILES) $(OBJS)

deepclean:
	make clean
	rm -rf data/*.txt data/*.mps *.lp

.cpp.o:
	$(CXX) $(CXXFLAGS) $(INCL) -c -o $@ `test -f '$<' || echo '$(SRCDIR)/'`$<

.cpp.obj:
	$(CXX) $(CXXFLAGS) $(INCL) -c -o $@ `if test -f '$<'; then $(CYGPATH_W) '$<'; else $(CYGPATH_W) '$(SRCDIR)/$<'; fi`

.c.o:
	$(CC) $(CFLAGS) $(INCL) -c -o $@ `test -f '$<' || echo '$(SRCDIR)/'`$<

.c.obj:
	$(CC) $(CFLAGS) $(INCL) -c -o $@ `if test -f '$<'; then $(CYGPATH_W) '$<'; else $(CYGPATH_W) '$(SRCDIR)/$<'; fi`
