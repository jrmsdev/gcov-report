CC := gcc
CFLAGS := -Wall -Wextra -pedantic -O0 -fprofile-arcs -ftest-coverage
GCOV := gcov5
TESTS != ls t???_*.c | sed 's/\.c/\.test/'
TESTS_RUN != ls t???_*.c | sed 's/\.c/\.run/'


.PHONY: check
check: build tests-run
	@CC=$(CC) GCOV=$(GCOV) ../scripts/run-gcov.sh >/dev/null
	@$(MAKE) gcovhtml
	@../bin/gcov-report.py --version
	@../scripts/tests-check.sh


.PHONY: check-coverage
check-coverage: build tests-run
	test -x ../venv/bin/coverage
	@rm -rf gcovhtml
	@mkdir -p gcovhtml
	@../venv/bin/coverage run ../bin/gcov-report.py --test-mode
	@../venv/bin/coverage report


.PHONY: build
build: $(TESTS)


.PHONY: tests-run
tests-run: $(TESTS_RUN)


.SUFFIXES:
.SUFFIXES: .c .test .run


.c.test:
	@$(CC) $(CFLAGS) -o $@ $<


.test.run:
	./$< >$@


.PHONY: gcovhtml
gcovhtml:
	@rm -rf gcovhtml
	@mkdir -p gcovhtml
	@../bin/gcov-report.py --test-mode


.PHONY: clean
clean:
	@rm -vf *.test *.run *.gcda *.gcno *.gcov .coverage
	@rm -vrf gcovhtml htmlcov
	@rm -vf shrun/*.diff shrun/*.test


.PHONY: htmlcov
htmlcov:
	test -x ../venv/bin/coverage
	../venv/bin/coverage html
