import time
from os import path

from . import tmpl, config


def write_html_head (out_f, title, main_class = "none"):
    with open (out_f, 'w') as fh:
        print (tmpl.TMPL_HEAD.format (title = title, css = tmpl.CSS,
                main_class = main_class), file = fh)
        fh.flush ()
        fh.close ()


def write_html_tail (out_f):
    fmt = {
        'doc_name': out_f.replace (config.htmldir + '/', '', 1),
        'doc_update': time.asctime (),
    }
    with open (out_f, 'a') as fh:
        print (tmpl.TMPL_TAIL.format (**fmt), file = fh)
        fh.flush ()
        fh.close ()


def write_gcov_html (src, dst, gcov):
    title = '%s %.2f%% done' % \
            (gcov.get ('attr.source'), gcov.get ('attr.__percent_ok'))
    write_html_head (dst, title)
    with open (dst, 'a') as fh:

        print (tmpl.html_navbar (), file = fh)
        print (tmpl.html_gcov_attribs (src, gcov), file = fh)

        for line in gcov['lines']:
            print (line['tmpl'].format (**line['data']), file = fh)

        fh.flush ()
        fh.close ()
    write_html_tail (dst)


def write_index (gcovdb):

    gcov_count = len (gcovdb)
    percent_total = 0
    total_expect = 100 * gcov_count
    total_ok = 0
    total_status = 'ok'
    dst = path.join (config.htmldir, 'index.html')


    with open (dst, 'a') as fh:

        for i in gcovdb:
            gcov = i['data']
            percent_total += gcov.get ('attr.__percent_ok', 0)
        total_ok = (percent_total * 100) / total_expect
        if total_ok <= config.percent_error:
            total_status = 'error'
        elif total_ok <= config.percent_warn:
            total_status = 'warn'

        write_html_head (dst, '%.2f%% done' % total_ok,
                main_class = 'index')

        print (tmpl.TMPL_GLOBAL_STATUS.format (
                percent = total_ok, status = total_status), file = fh)
        print ("scanned files:", gcov_count, file = fh)

        for i in gcovdb:
            gcov_src = i['src']
            gcov = i['data']

            status = gcov.get ('attr.status', None)
            print (tmpl.TMPL_FILE_INDEX_STATUS.format (
                    sep = 7 - len (status),
                    sep_char = ' ',
                    status = status), file = fh, end = '')

            seplen = (50 - len (gcov_src))
            if seplen < 0:
                seplen = 0
            print (tmpl.TMPL_FILE_INDEX.format (
                    status = status,
                    status_info = gcov.get ('attr.status.info', None),
                    sep = seplen,
                    sep_char = ' ',
                    file_href = tmpl.html_link (gcov_src, gcov_src)), file = fh)

        fh.flush ()
        fh.close ()

    write_html_tail (dst)
    print ("index:", dst)