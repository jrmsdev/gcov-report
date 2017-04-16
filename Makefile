PREFIX ?= /opt/pkg
INSTALL_EXE := install -v -m 0555
INSTALL_F := install -v -m 0444
DEST_BINDIR := $(DESTDIR)$(PREFIX)/bin
DEST_LIBDIR := $(DESTDIR)$(PREFIX)/lib/gcovreport
DEST_LICDIR := $(DESTDIR)$(PREFIX)/share/licenses/gcov-report


.PHONY: build
build:
	@python3 -m compileall lib/gcovreport


.PHONY: clean
clean:
	@rm -rfv gcovhtml lib/gcovreport/__pycache__
	@$(MAKE) -C tests clean


.PHONY: installdirs
installdirs:
	@mkdir -vp $(DEST_BINDIR) $(DEST_LIBDIR) $(DEST_LICDIR)
	@mkdir -vp $(DEST_LIBDIR)/__pycache__


.PHONY: install
install: build installdirs
	@$(INSTALL_EXE) bin/gcov-report.py $(DEST_BINDIR)/gcov-report
	@$(INSTALL_F) lib/gcovreport/*.py $(DEST_LIBDIR)
	@$(INSTALL_F) lib/gcovreport/__pycache__/*.pyc $(DEST_LIBDIR)/__pycache__
	@$(INSTALL_F) LICENSE $(DEST_LICDIR)


.PHONY: uninstall
uninstall:
	@rm -vrf $(DEST_BINDIR)/gcov-report $(DEST_LIBDIR) $(DEST_LICDIR)


.PHONY: check
check:
	@$(MAKE) -C tests check
