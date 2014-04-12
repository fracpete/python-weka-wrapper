# Makefile for Sphinx documentation
#

SRCDIR        = src
BUILDDIR      = build
DISTDIR       = dist
LIBDIR        = ../lib

all: clean compile dist

clean:
	rm -rf $(BUILDDIR)
	rm -rf $(DISTDIR)
	find -name "*~" -delete

compile:
	mkdir -p $(BUILDDIR)
	find $(SRCDIR) -name "*.java" -exec javac -classpath $(LIBDIR)/weka.jar -d $(BUILDDIR) {} \;

dist:
	mkdir -p $(DISTDIR)
	jar -cf $(DISTDIR)/python-weka-wrapper.jar -C $(BUILDDIR) weka

