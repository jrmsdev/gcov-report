class Tmpl:
    txt = None
    _d = None
    _dopts = None

    def __init__ (self):
        self._d = dict ()
        self._dopts = list ()

    def format (self):
        return self.txt.format (**self._d)

    def set (self, opt, val):
        if opt in self._dopts:
            raise RuntimeError ("Tmpl data option '%s' already set!" % opt)
        self._d[opt] = val
        self._dopts.append (opt)


class TMPL_HEAD(Tmpl):
    txt = '''<!doctype html>
<html>
<head>
    {css}
    <title>gcov-report - {title}</title>
</head>
<body>'''


class TMPL_TAIL(Tmpl):
    txt = '''<footer>
{doc_name}: {doc_update}<br>
<a target="_blank"
   href="{project_url}">gcov-report</a> v{appversion}
</footer>
</body>
</html>'''


class TMPL_CODE_NORMAL(Tmpl):
    txt = '<span class="normal">{lineno:>4}: {content}</span>'


class TMPL_CODE_NOEXEC(Tmpl):
    txt = '<span class="noexec">{lineno:>4}: {content}</span>'


class TMPL_CODE_EXEC(Tmpl):
    txt = '<span class="exec">{lineno:>4}: {content}</span>'


class TMPL_GCOV_INFO(Tmpl):
    txt = '<span class="status info">{content}</span>'


class TMPL_GCOV_ATTRIB(Tmpl):
    txt = '''
<span class="status_{attr_class}">{attr_key}: {attr_val}</span><br>
'''


class TMPL_LINK(Tmpl):
    txt = '<a href="{href}">{content}</a>'


class TMPL_FILE_INDEX_START(Tmpl):
    txt = '<ol>'


class TMPL_FILE_INDEX_STATUS(Tmpl):
    txt = '''
<li class="index_entry">
    <span class="status_{status}">|{status_info:|>7}|</span>
    <span>{file_href}</span>
    <span class="filename">{source}</span>
</li>
'''


class TMPL_FILE_INDEX_END(Tmpl):
    txt = '</ol>'


class TMPL_GLOBAL_STATUS(Tmpl):
    txt = '''<p>
global status: <span class="status_{status}">{percent:.2f}% done</span><br>
scanned files: {filesno}
</p>
'''


class TMPL_DIV_START(Tmpl):
    txt = '<div class="div_{div_class}">'


class TMPL_DIV_END(Tmpl):
    txt = '</div>'


#
# -- html helpers
#


def html_link (href, content):
    t = TMPL_LINK()
    t.set ('href', "%s.html" % href)
    t.set ('content', content)
    return t.format ()


def html_navbar ():
    s = '<div class="navbar">'
    t = TMPL_LINK()
    t.set ('href', './index.html')
    t.set ('content', '<b>index</b>')
    s += t.format ()
    return "%s</div>" % s


def html_gcov_attribs (src, gcov):
    s = "[no attribs]" + src
    atclass = "normal"

    if len (gcov.attribs) > 0:
        t = TMPL_GCOV_ATTRIB()
        t.set ('attr_class', atclass)
        t.set ('attr_key', 'gcov')
        t.set ('attr_val', src)
        s = t.format ()

        for kn in gcov.attribs.keys ():
            try:

                if kn.startswith ('__'):
                    continue

                elif kn == "source.lines.noexec":
                    if 0 != int (gcov.attribs.get (kn)):
                        atclass = "error"

                elif kn == "status":
                    atclass = gcov.attribs.get (kn)

                elif kn == "status.info":
                    atclass = gcov.attribs.get ('status', atclass)

                elif kn == "source":
                    atclass = "info"

                t = TMPL_GCOV_ATTRIB()
                t.set ('attr_class', atclass)
                t.set ('attr_key', kn)
                t.set ('attr_val', gcov.attribs.get (kn))
                s += t.format ()

            except IndexError as e: # pragma: no cover

                print ("gcov_attribs:", src, "IndexError:", str (e))

    return s


CSS = '''<style>
    body {
        background-color: #000000;
        color: #666666;
        font-family: monospace;
        font-size: 1.2em;
        padding: 1em 1em;
        margin: 0;
        line-height: 1.3em;
    }
    a {
        color: #0000cc;
    }
    span.noexec {
        color: #cc0000;
    }
    span.exec {
        color: #00ee00;
    }
    span.normal {
        color: #008800;
    }
    span.info {
        color: #aa00bb;
    }
    footer {
        font-size: 0.7em;
        line-height: 1.1em;
    }
    footer a {
        color: #666666;
    }
    div.navbar {
        margin-bottom: 1em;
    }
    .status {
        font-size: 0.7em;
    }
    .status_error {
        color: #cc0000;
    }
    .status_info {
        color: #00cccc;
    }
    .status_warn {
        color: #cccc33;
    }
    .status_ok {
        color: #00cc00;
    }
    .filename {
        color: #cccccc;
    }
    li.index_entry {
        margin-bottom: 0.3em;
    }
    </style>'''
