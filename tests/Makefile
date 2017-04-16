CC := gcc
CFLAGS := -Wall -Wextra -pedantic -O0 -fprofile-arcs -ftest-coverage
GCOV := gcov5
TESTS != ls *.c | sed 's/\.c/\.test/g'
TESTS_RUN != ls *.c | sed 's/\.c/\.run/g'


.PHONY: check
check: build tests-run
	@CC=$(CC) GCOV=$(GCOV) ../scripts/run-gcov.sh >/dev/null
	@$(MAKE) gcovhtml
	@../scripts/tests-check.sh


.PHONY: build
build: $(TESTS)


.PHONY: tests-run
tests-run: $(TESTS_RUN)


.SUFFIXES:
.SUFFIXES: .c .test .run


.c.test:
	$(CC) $(CFLAGS) -o $@ $<


.test.run:
	./$< >$@


.PHONY: gcovhtml
gcovhtml:
	@rm -rf gcovhtml
	@mkdir -p gcovhtml
	@../bin/gcov-report.py --test-mode


.PHONY: clean
clean:
	@rm -vf *.test *.run *.gcda *.gcno *.gcov
	@rm -vrf gcovhtml
