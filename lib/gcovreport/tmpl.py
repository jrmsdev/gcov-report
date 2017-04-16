#
# -- HTML templates
#

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

TMPL_HEAD = '''<!doctype html>
<html>
<head>
    {css}
    <title>gcov-report - {title}</title>
</head>
<body>'''

TMPL_TAIL = '''<footer>
{doc_name}: {doc_update}<br>
<a target="_blank"
   href="https://github.com/jrmsdev/gcov-report">gcov-report</a> v{appversion}
</footer>
</body>
</html>'''

TMPL_CODE_NORMAL = '<span class="normal">{lineno:>4}: {content}</span>'

TMPL_CODE_NOEXEC = '<span class="noexec">{lineno:>4}: {content}</span>'

TMPL_CODE_EXEC = '<span class="exec">{lineno:>4}: {content}</span>'

TMPL_GCOV_INFO = '<span class="status info">{content}</span>'

TMPL_GCOV_ATTRIB = '''
<span class="status_{attr_class}">{attr_key}: {attr_val}</span><br>
'''

TMPL_LINK = '<a href="{href}">{content}</a>'

TMPL_FILE_INDEX_START = '<ol>'
TMPL_FILE_INDEX_STATUS = '''
<li class="index_entry">
    <span class="status_{status}">|{status_info:|>7}|</span>
    <span>{file_href}</span>
    <span class="filename">{source}</span>
</li>
'''
TMPL_FILE_INDEX_END = '</ol>'

TMPL_GLOBAL_STATUS = '''<p>
global status: <span class="status_{status}">{percent:.2f}% done</span><br>
scanned files: {filesno}
</p>
'''

TMPL_DIV_START = '<div class="div_{div_class}">'

TMPL_DIV_END = '</div>'

#
# -- html helpers
#

def html_link (href, content):
    return TMPL_LINK.format (href = href + '.html', content = content)


def html_navbar ():
    s = '<div class="navbar">'
    s += TMPL_LINK.format (href = './index.html', content = '<b>index</b>')
    return "%s</div>" % s


def html_gcov_attribs (src, gcov):
    s = "[no attribs]" + src
    attr_found = False
    for k in sorted (gcov.keys ()):
        if k.startswith ('attr.'):
            atclass = "normal"
            if not attr_found:
                attr_found = True
                s = TMPL_GCOV_ATTRIB.format (
                        attr_class = atclass, attr_key = 'gcov', attr_val = src)
            try:
                kn = '.'.join (k.split ('.')[1:])
                kv = gcov.get ('attr.' + kn, None)

                if kn.startswith ('__'):
                    continue

                elif kn == "source.lines.noexec":
                    if 0 != int (kv):
                        atclass = "error"

                elif kn == "status":
                    atclass = kv

                elif kn == "status.info":
                    atclass = gcov.get ('attr.status', atclass)

                elif kn == "source":
                    atclass = "info"

                s += TMPL_GCOV_ATTRIB.format (
                        attr_class = atclass, attr_key = kn, attr_val = kv)
            except IndexError as e:
                print ("gcov_attribs:", src, "IndexError:", str (e))

    return s
