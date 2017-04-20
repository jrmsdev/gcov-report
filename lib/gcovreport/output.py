import html
from os import path
from . import tmpl, config, version, utils


def write_html_head (out_f, title, div_class):
    with open (out_f, 'w') as fh:

        t = tmpl.TMPL_HEAD()
        t.set ('title', title)
        t.set ('css', tmpl.CSS)
        print (t.format (), file = fh)

        t = tmpl.TMPL_DIV_START()
        t.set ('div_class', div_class)
        print (t.format (), file = fh)

        fh.flush ()
        fh.close ()


def write_html_tail (out_f):
    with open (out_f, 'a') as fh:
        print (tmpl.TMPL_DIV_END().format (), file = fh)
        t = tmpl.TMPL_TAIL()
        t.set ('appversion', version.get_string ())
        t.set ('doc_name', out_f.replace (config.htmldir + '/', '', 1))
        t.set ('doc_update', utils.asctime ())
        t.set ('project_url', version.project_url ())
        print (t.format (), file = fh)
        fh.flush ()
        fh.close ()


def write_gcov_html (src, dst, gcov):
    title = '%s %.2f%% done' % \
            (gcov.attribs.get ('source'), gcov.attribs.get ('__percent_ok'))
    write_html_head (dst, title, 'gcov')
    with open (dst, 'a') as fh:

        print (tmpl.html_navbar (), file = fh)

        print ('<p>', file = fh)
        print (tmpl.html_gcov_attribs (src, gcov), file = fh)
        print ('</p>', file = fh)

        print ('<pre>', file = fh)
        for line in gcov.lines:
            print (line.format (), file = fh)
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
            percent_total += gcov.attribs.get ('__percent_ok', 0)
        total_ok = (percent_total * 100) / total_expect

        if total_ok <= config.percent_error:
            total_status = 'error'
        elif total_ok <= config.percent_warn:
            total_status = 'warn'

        write_html_head (dst, '%.2f%% done' % total_ok, 'index')

        t = tmpl.TMPL_GLOBAL_STATUS()
        t.set ('filesno', gcov_count)
        t.set ('percent', total_ok)
        t.set ('status', total_status)
        print (t.format (), file = fh)

        print (tmpl.TMPL_FILE_INDEX_START().format (), file = fh)

        for gcov in gcovdb:
            attr_src = gcov.attribs.get ('source')

            t = tmpl.TMPL_FILE_INDEX_STATUS()
            t.set ('source', attr_src)
            t.set ('file_href', tmpl.html_link (path.basename (attr_src),
                            html.escape ('>>>')))
            t.set ('status_info', gcov.attribs.get ('status.info'))
            t.set ('status', gcov.attribs.get ('status'))
            print (t.format (), file = fh)

        print (tmpl.TMPL_FILE_INDEX_END().format (), file = fh)

        fh.flush ()
        fh.close ()

    write_html_tail (dst)
    print ("index:", dst)
