#
# -- HTML templates
#

CSS = '''<style>
    body {
        background-color: #000000;
        color: #666666;
        font-family: monospace;
        font-size: 14px;
        padding: 1% 1%;
        margin: 0;
        line-height: 1.3em;
    }
    a {
        color: #0000cc;
    }
    code.noexec {
        color: #cc0000;
    }
    code.exec {
        color: #00ee00;
    }
    code.normal {
        color: #008800;
    }
    code.info {
        color: #aa00bb;
    }
    pre.index {
        line-height: 1.5em;
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
    </style>'''

TMPL_HEAD = '''<!doctype html>
<html>
<head>
    {css}
    <title>jcaslib tests coverage - {title}</title>
</head>
<body>
<pre class="{main_class}">'''

TMPL_TAIL = '''</pre>
<pre class="footer">
<small><small>{doc_name}: {doc_update}</small></small>
</pre>
</body>
</html>'''

TMPL_FILE_SUMM = '{idx:5}: {lines_exec:15} <i>{name}</i>'

TMPL_CODE_NORMAL = '<code class="normal">{lineno:>4}: {content}</code>'

TMPL_CODE_NOEXEC = '<code class="noexec">{lineno:>4}: {content}</code>'

TMPL_CODE_EXEC = '<code class="exec">{lineno:>4}: {content}</code>'

TMPL_GCOV_INFO = '<code class="info"><small><small>{content}</small></small></code>'

TMPL_GCOV_ATTRIB = '<small class="status_{attr_class}">{attr_key}: {attr_val}</small>'

TMPL_LINK = '<a href="{href}">{content}</a>'

TMPL_FILE_INDEX_STATUS = '{sep_char:{sep}}<span class="status_{status}">{status}</span> '

TMPL_FILE_INDEX = '<b>{file_href}</b>{sep_char:{sep}} <span class="status_{status}">{status_info}</span>'

TMPL_GLOBAL_STATUS = 'global status: <span class="status_{status}">{percent:.2f}% done</span>'

#
# -- html helpers
#

def html_link (href, content):
    return TMPL_LINK.format (href = href + '.html', content = content)


def html_navbar ():
    s = TMPL_LINK.format (href = './index.html', content = 'index')
    return "<b>%s</b>\n" % s


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
                s += "\n"
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
                s += "\n"
            except IndexError as e:
                print ("gcov_attribs:", src, "IndexError:", str (e))

    return s + "\n"
