COVERAGE_CMD ?=
PREFIX ?= /opt/pkg
VENVDIR ?= $(PREFIX)/venv.py3/gcov-report


.PHONY: check
check:
	@../bin/gcov-report.py --version
	@rm -rf tmpdir
	@mkdir -p tmpdir
	@COVERAGE_CMD='$(COVERAGE_CMD)' ../scripts/tests-check.sh


.PHONY: check-coverage
check-coverage:
	test -x $(VENVDIR)/bin/coverage
	@rm -vf .coverage
	@$(MAKE) check COVERAGE_CMD='$(VENVDIR)/bin/coverage run'
	@$(VENVDIR)/bin/coverage report


.PHONY: clean
clean:
	@rm -vf .coverage
	@rm -vrf htmlcov tmpdir


.PHONY: htmlcov
htmlcov:
	test -x $(VENVDIR)/bin/coverage
	$(VENVDIR)/bin/coverage html

# -- gen .gcov files

CC := gcc
CFLAGS := -Wall -Wextra -pedantic -O0 -fprofile-arcs -ftest-coverage
GCOV := gcov5
TESTS != ls t???_*.c | sed 's/\.c/\.test/'
TESTS_RUN != ls t???_*.c | sed 's/\.c/\.run/'

.PHONY: gcovgen
gcovgen: gcovbuild gcovrun
	@CC=$(CC) GCOV=$(GCOV) ../scripts/run-gcov.sh >/dev/null 2>/dev/null

.PHONY: gcovbuild
gcovbuild: $(TESTS)

.PHONY: gcovrun
gcovrun: $(TESTS_RUN)

.SUFFIXES:
.SUFFIXES: .c .test .run

.c.test:
	@$(CC) $(CFLAGS) -o $@ $<

.test.run:
	@./$< >$@
