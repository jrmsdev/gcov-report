import html
from os import path
from . import tmpl
from .. import config, version, utils, debug


def write_html_head (out_f, title, div_class):
    debug.log ("write_html_head:", out_f)
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
    debug.log ("write_html_tail:", out_f)
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
        debug.log ("write_gcov_html:", src, dst)
        debug.log ("write_gcov_html:", repr (gcov))

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


def write_index (gcovdb, dbstat):

    dst = path.join (config.htmldir, 'index.html')
    gcov_count = len (gcovdb)

    with open (dst, 'a') as fh:

        write_html_head (dst, '%.2f%% done' % dbstat.total_ok, 'index')
        debug.log ("write_index:", dst)

        t = tmpl.TMPL_GLOBAL_STATUS()
        t.set ('filesno', gcov_count)
        t.set ('percent', dbstat.total_ok)
        t.set ('status', dbstat.total_status)
        print (t.format (), file = fh)

        print (tmpl.TMPL_FILE_INDEX_START().format (), file = fh)

        for gcov in gcovdb:

            gcov_src = path.basename (gcov.attribs.get ('gcov'))
            debug.log ("write_index gcov src:", gcov_src)

            t = tmpl.TMPL_FILE_INDEX_STATUS()
            t.set ('source', html.escape (gcov.attribs.get ('source')))
            t.set ('file_link', tmpl.html_link (
                    html.escape (
                        gcov_src.replace('.gcov', '').replace('#', '%23')
                    ),
                    html.escape ('>>>')))
            t.set ('status_info', gcov.attribs.get ('status.info'))
            t.set ('status', gcov.attribs.get ('status'))
            print (t.format (), file = fh)

        print (tmpl.TMPL_FILE_INDEX_END().format (), file = fh)

        fh.flush ()
        fh.close ()

    write_html_tail (dst)
    #~ print ("index:", path.basename (dst))
