import re
import html
from os import path
from . import config, tmpl, output

# -- parse gcov regexs
re_gcov_attr_source = re.compile ('^\s*-:\s*0:Source:(.*)$')
re_gcov_attr_runs = re.compile ('^\s*-:\s*0:Runs:(\d*)$')
re_gcov_normal = re.compile ('^\s*-:\s*(\d*):(.*)$')
re_gcov_noexec = re.compile ('^\s*#####:\s*(\d*):(.*)$')
re_gcov_exec = re.compile ('^\s*\d*:\s*(\d*):(.*)$')
re_gcov_info = re.compile ('^(\w+\s.*)$')


def parse_gcov (src):

    def new_code_line (gcov, tmpl, lineno, content):
        gcov['lines'].append ({
            'tmpl': tmpl,
            'data': {'lineno': lineno, 'content': content},
        })

    def new_line (gcov, tmpl, content):
        gcov['lines'].append ({'tmpl': tmpl, 'data': {'content': content}})

    def update_attribs (gcov, attr):
        for k in attr.keys ():
            gcov['attr.' + k] = attr.get (k)

    def gcov_status (attr):
        lines = attr.get ('source.lines', 0)
        lines_normal = attr.get ('source.lines.normal', 0)
        lines_exec = attr.get ('source.lines.exec', 0)
        lines_noexec = attr.get ('source.lines.noexec', 0)

        if lines != (lines_normal + lines_exec + lines_noexec):
            attr['status.info'] = "lines count error"
            attr['status'] = "error"
            attr['status.percent_ok'] = 0
        else:
            percent_ok = ((lines_normal + lines_exec) * 100) / lines
            attr['status.info'] = "done: {:>6.2f}%".format (percent_ok)
            if percent_ok <= config.percent_error:
                attr['status'] = 'error'
            elif percent_ok <= config.percent_warn:
                attr['status'] = 'warn'
            attr['__percent_ok'] = percent_ok

    dst = path.join (config.htmldir, src)
    dst = dst.replace('.gcov', '.html')
    gcov = dict(lines = list (), status_info = '')

    # XXX: not sure why yet but it needs to start as 1 instead of 0
    gcov_lines = 1
    attr = {
        'source.lines': 0,
        'source.lines.normal': 0,
        'source.lines.exec': 0,
        'source.lines.noexec': 0,
        'status': 'ok',
        'status.info': '',
    }

    print ("parse:", src, "->", dst)

    with open (src, 'r') as fh:
        for line in fh.readlines ():

            m = None
            gcov_lines += 1

            m = re_gcov_attr_source.match (line)
            if m:
                gcov['attr.source'] = html.escape (m.group (1))
                continue

            m = re_gcov_attr_runs.match (line)
            if m:
                gcov['attr.runs'] = html.escape (m.group (1))
                continue

            m = re_gcov_normal.match (line)
            if m:
                idx = m.group (1)
                if idx != "0":
                    attr['source.lines'] += 1
                    attr['source.lines.normal'] += 1
                    new_code_line (gcov, tmpl.TMPL_CODE_NORMAL, idx,
                            html.escape (m.group (2)))
                continue

            m = re_gcov_noexec.match (line)
            if m:
                attr['source.lines'] += 1
                attr['source.lines.noexec'] += 1
                idx = m.group (1)
                new_code_line (gcov, tmpl.TMPL_CODE_NOEXEC, idx,
                        html.escape (m.group (2)))
                continue

            m = re_gcov_exec.match (line)
            if m:
                attr['source.lines'] += 1
                attr['source.lines.exec'] += 1
                idx = m.group (1)
                new_code_line (gcov, tmpl.TMPL_CODE_EXEC, idx,
                        html.escape (m.group (2)))
                continue

            m = re_gcov_info.match (line)
            if m:
                new_line (gcov, tmpl.TMPL_GCOV_INFO, html.escape (m.group (1)))
                continue

            if m is None:
                print ("parse:", src, "unkown line:", gcov_lines)

        fh.close ()

    gcov_status (attr)
    update_attribs (gcov, attr)
    output.write_gcov_html (src, dst, gcov)

    return gcov
