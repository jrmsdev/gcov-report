# gcov-report

Create an HTML report about generated gcov data.

## Install

    $ git clone https://github.com/jrmsdev/gcov-report.git
    $ cd gcov-report
    $ make install PREFIX=/usr/local

By default PREFIX is set as /opt/pkg.

## Usage

Just run the command inside the directory with all the .gcov files in it.
The output directory has to be manually created first, the script refuses to
run if it doesn't exists... Trying to avoid messing things around automatically.

    $ cd gcov-data-dir
    $ mkdir gcovhtml
    $ gcov-report
