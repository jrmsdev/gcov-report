.PHONY: build
build:
	@python3 -m compileall lib/gcovreport


.PHONY: clean
clean:
	@rm -rfv gcovhtml lib/gcovreport/__pycache__
