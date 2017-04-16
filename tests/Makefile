CC := gcc
CFLAGS := -Wall -Wextra -pedantic -O0 -fprofile-arcs -ftest-coverage
GCOV := gcov5
TESTS != ls t???_*.c | sed 's/\.c/\.test/'
TESTS_RUN != ls t???_*.c | sed 's/\.c/\.run/'
SH_TESTS != ls t???_*.sh
SH_TESTS_RUN != ls t???_*.sh | sed 's/\.sh/\.shrun/'


.PHONY: check
check: build tests-run
	@CC=$(CC) GCOV=$(GCOV) ../scripts/run-gcov.sh >/dev/null
	@$(MAKE) gcovhtml
	@../bin/gcov-report.py --version
	@../scripts/tests-check.sh


.PHONY: build
build: $(TESTS)


.PHONY: tests-run
tests-run: $(TESTS_RUN) $(SH_TESTS_RUN)


.SUFFIXES:
.SUFFIXES: .c .test .run .sh .shrun


.c.test:
	@$(CC) $(CFLAGS) -o $@ $<


.test.run:
	./$< >$@


.sh.shrun:
	./$< >$@


.PHONY: gcovhtml
gcovhtml:
	@rm -rf gcovhtml
	@mkdir -p gcovhtml
	@../bin/gcov-report.py --test-mode


.PHONY: clean
clean:
	@rm -vf *.test *.run *.gcda *.gcno *.gcov .coverage *.shrun *.diff
	@rm -vrf gcovhtml htmlcov


.PHONY: check-coverage
check-coverage: check
	test -x ../venv/bin/coverage
	@rm -rf gcovhtml
	@mkdir -p gcovhtml
	@../venv/bin/coverage run ../bin/gcov-report.py --test-mode
	@../venv/bin/coverage report


.PHONY: htmlcov
htmlcov:
	test -x ../venv/bin/coverage
	../venv/bin/coverage html
