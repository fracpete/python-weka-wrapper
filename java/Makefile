# Makefile for additional class for python-weka-wrapper
#
# Author: Fracpete (fracpete at gmail dot com)

SRCDIR        = src
BUILDDIR      = build
DISTDIR       = dist
LIBDIR        = ../lib

all: clean compile dist

clean:
	@echo cleaning up...
	rm -rf $(BUILDDIR)
	rm -rf $(DISTDIR)
	find -name "*~" -delete

compile:
	@echo compiling source files...
	mkdir -p $(BUILDDIR)
	find $(SRCDIR) -name "*.java" -exec javac -classpath $(LIBDIR)/weka.jar -d $(BUILDDIR) {} \;

dist:
	@echo creating jar archive...
	mkdir -p $(DISTDIR)
	jar -cf $(DISTDIR)/python-weka-wrapper.jar -C $(BUILDDIR) weka
	cp $(DISTDIR)/python-weka-wrapper.jar $(LIBDIR)

