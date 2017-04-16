from os import path
from . import tmpl, config, version, utils


def write_html_head (out_f, title, div_class):
    with open (out_f, 'w') as fh:
        print (tmpl.TMPL_HEAD.format (title = title,
                css = tmpl.CSS), file = fh)
        print (tmpl.TMPL_DIV_START.format (div_class = div_class), file = fh)
        fh.flush ()
        fh.close ()


def write_html_tail (out_f):
    fmt = {
        'appversion': version.get_string (),
        'doc_name': out_f.replace (config.htmldir + '/', '', 1),
        'doc_update': utils.asctime (),
        'project_url': version.project_url (),
    }
    with open (out_f, 'a') as fh:
        print (tmpl.TMPL_DIV_END, file = fh)
        print (tmpl.TMPL_TAIL.format (**fmt), file = fh)
        fh.flush ()
        fh.close ()


def write_gcov_html (src, dst, gcov):
    title = '%s %.2f%% done' % \
            (gcov.get ('attr.source'), gcov.get ('attr.__percent_ok'))
    write_html_head (dst, title, 'gcov')
    with open (dst, 'a') as fh:

        print (tmpl.html_navbar (), file = fh)

        print ('<p>', file = fh)
        print (tmpl.html_gcov_attribs (src, gcov), file = fh)
        print ('</p>', file = fh)

        print ('<pre>', file = fh)
        for line in gcov['lines']:
            print (line['tmpl'].format (**line['data']), file = fh)
        print ('</pre>', file = fh)

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

        for gcov in gcovdb:
            percent_total += gcov.get ('attr.__percent_ok', 0)
        total_ok = (percent_total * 100) / total_expect

        if total_ok <= config.percent_error: # pragma: no cover
            total_status = 'error'
        elif total_ok <= config.percent_warn:
            total_status = 'warn'

        write_html_head (dst, '%.2f%% done' % total_ok, 'index')

        print (tmpl.TMPL_GLOBAL_STATUS.format (filesno = gcov_count,
                percent = total_ok, status = total_status), file = fh)

        print (tmpl.TMPL_FILE_INDEX_START, file = fh)

        for gcov in gcovdb:
            attr_src = gcov.get ('attr.source')

            print (tmpl.TMPL_FILE_INDEX_STATUS.format (
                    source = attr_src,
                    file_href = tmpl.html_link (path.basename (attr_src), '>>>'),
                    status_info = gcov.get ('attr.status.info', None),
                    status = gcov.get ('attr.status', None)), file = fh)

        print (tmpl.TMPL_FILE_INDEX_END, file = fh)

        fh.flush ()
        fh.close ()

    write_html_tail (dst)
    print ("index:", dst)
