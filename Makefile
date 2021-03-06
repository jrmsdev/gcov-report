PREFIX ?= /opt/pkg
INSTALL_EXE := install -v -m 0555
INSTALL_F := install -v -m 0444
DEST_BINDIR := $(DESTDIR)$(PREFIX)/bin
DEST_LIBDIR := $(DESTDIR)$(PREFIX)/lib/gcovreport
DEST_LICDIR := $(DESTDIR)$(PREFIX)/share/licenses/gcov-report

VENVDIR ?= $(PREFIX)/venv.py3/gcov-report
PYCMD ?= python3


.PHONY: build
build:
	@$(PYCMD) -m compileall lib/gcovreport


.PHONY: clean
clean:
	@rm -rfv dist/release.txt
	@rm -rfv lib/gcovreport/__pycache__ lib/gcovreport/*/__pycache__
	@$(MAKE) -C tests clean


.PHONY: installdirs
installdirs:
	@mkdir -vp $(DEST_BINDIR) $(DEST_LIBDIR) $(DEST_LICDIR)
	@mkdir -vp $(DEST_LIBDIR)/htmlx
	@mkdir -vp $(DEST_LIBDIR)/gcov


.PHONY: install
install: build installdirs dist/release.txt
	@$(INSTALL_EXE) bin/gcov-report.py $(DEST_BINDIR)/gcov-report
	@$(INSTALL_F) lib/gcovreport/*.py $(DEST_LIBDIR)
	@$(INSTALL_F) lib/gcovreport/htmlx/*.py $(DEST_LIBDIR)/htmlx
	@$(INSTALL_F) lib/gcovreport/gcov/*.py $(DEST_LIBDIR)/gcov
	@$(PYCMD) -m compileall $(DEST_LIBDIR)
	@$(INSTALL_F) LICENSE $(DEST_LICDIR)
	@$(INSTALL_F) dist/release.txt $(DEST_LIBDIR)


.PHONY: uninstall
uninstall:
	@rm -vrf $(DEST_BINDIR)/gcov-report $(DEST_LIBDIR) $(DEST_LICDIR)


.PHONY: check
check:
	@$(MAKE) -C tests check


.PHONY: venv
venv:
	@$(PYCMD) -m venv --symlinks $(VENVDIR)
	@$(VENVDIR)/bin/pip check
	@$(VENVDIR)/bin/pip install coverage


.PHONY: check-coverage
check-coverage: build venv
	@$(MAKE) -C tests check-coverage


.PHONY: distclean
distclean: clean
	@rm -vrf dist


dist/release.txt: scripts/mk-releasetxt.sh
	@mkdir -vp dist
	@./scripts/mk-releasetxt.sh


.PHONY: dist
dist: dist/release.txt
	@mkdir -vp dist
	@rm -rf dist/work
	@$(MAKE) install DESTDIR=dist/work PREFIX=$(PREFIX)
	@./scripts/mkdist-tar.sh
