import re
import html
from os import path

from .. import config, debug
from ..htmlx import  tmpl, output

re_gcov_attr_source = re.compile ('^\s+-:\s+0:Source:(.+)$')
re_gcov_attr_runs = re.compile ('^\s+-:\s+0:Runs:(\d+)$')
re_gcov_normal = re.compile ('^\s+-:\s+(\d+):(.*)$')
re_gcov_noexec = re.compile ('^\s+#####:\s+(\d+):(.+)$')
re_gcov_exec = re.compile ('^\s+(\d+):\s+(\d+):(.+)$')
re_gcov_info = re.compile ('^(\w+\s.*)$')


class GcovLine:
    tmpl = None

    class data:
        lineno = None
        content = None
        exec_count = '0'

    def __init__ (self, tmplclass, content, lineno, exec_count):
        self.tmpl = tmplclass()
        self.tmpl.set ('lineno', lineno)
        self.tmpl.set ('content', content)
        self.tmpl.set ('exec_count', exec_count)

    def format (self):
        return self.tmpl.format ()


class GcovAttribs:
    _d = None

    def __init__ (self):
        self._d = dict ()

    def __str__ (self):
        return "{}".format (str (sorted (
                self._d.items ())).replace ('), ', '\n'))

    def get (self, k, default = None):
        return self._d.get (k, default)

    def __getitem__ (self, k, default = None):
        return self.get (k, default)

    def set (self, k, v):
        self._d[k] = v

    def __setitem__ (self, k, v):
        self.set (k, v)

    def update (self, attribs):
        self._d.update (attribs)

    def keys (self):
        return sorted (self._d.keys ())

    def __len__ (self):
        return len (self._d)


class Gcov:
    lines = None
    attribs = None

    def __init__ (self, filename):
        self.lines = list()
        self.attribs = GcovAttribs()
        self.attribs.set ('gcov', filename)

    def __repr__(self):
        return "<Gcov{}>".format (str (self.attribs))

    def __str__(self):
        return "{:48s} {:<6d} {:<6d} {:<5s} {:>8s}".format (
            self.attribs.get ('source'),
            self.attribs.get ('source.lines'),
            self.attribs.get ('source.lines.noexec'),
            self.attribs.get ('status'),
            self.attribs.get ('status.info'),
        )

    def newline (self, tmpl, content, lineno = None, exec_count = '0'):
        self.lines.append (GcovLine (tmpl, content, lineno, exec_count))

    def status (self):
        lines = self.attribs.get ('source.lines', 0)
        lines_normal = self.attribs.get ('source.lines.normal', 0)
        lines_exec = self.attribs.get ('source.lines.exec', 0)
        lines_noexec = self.attribs.get ('source.lines.noexec', 0)

        if lines != (lines_normal + lines_exec + lines_noexec):
            self.attribs.set ('status.info', "lines count error")
            self.attribs.set ('status', "error")
            self.attribs.set ('status.percent_ok', 0)
        else:
            percent_ok = ((lines_normal + lines_exec) * 100) / lines
            self.attribs.set ('status.info', "{:.2f}%".format (percent_ok))
            if percent_ok <= config.percent_error:
                self.attribs.set ('status', 'error')
            elif percent_ok <= config.percent_warn:
                self.attribs.set ('status', 'warn')
            self.attribs.set ('__percent_ok', percent_ok)


def parse_gcov (src):
    dst = path.join (config.htmldir, path.basename (src))
    dst = dst.replace('.gcov', '.html')

    debug.log ("parse_gcov:", src, dst)

    gcov = Gcov (src)
    gcov.attribs.update ({
        'source.lines': 0,
        'source.lines.normal': 0,
        'source.lines.exec': 0,
        'source.lines.noexec': 0,
        'status': 'ok',
        'status.info': '',
    })

    # XXX: not sure why yet but it needs to start as 1 instead of 0
    gcov_lines = 1

    #~ print ("parse:", path.basename (src), "->", path.basename (dst))

    with open (src, 'r') as fh:
        for line in fh.readlines ():

            m = None
            gcov_lines += 1

            m = re_gcov_attr_source.match (line)
            if m:
                gcov.attribs.set ('source', html.escape (m.group (1)))
                continue

            m = re_gcov_attr_runs.match (line)
            if m:
                gcov.attribs.set ('runs', html.escape (m.group (1)))
                continue

            m = re_gcov_normal.match (line)
            if m:
                idx = m.group (1)
                if idx != "0":
                    gcov.attribs['source.lines'] += 1
                    gcov.attribs['source.lines.normal'] += 1
                    gcov.newline (tmpl.TMPL_CODE_NORMAL,
                            html.escape (m.group (2)), idx, " ")
                continue

            m = re_gcov_noexec.match (line)
            if m:
                gcov.attribs['source.lines'] += 1
                gcov.attribs['source.lines.noexec'] += 1
                idx = m.group (1)
                gcov.newline (tmpl.TMPL_CODE_NOEXEC,
                        html.escape (m.group (2)), idx)
                continue

            m = re_gcov_exec.match (line)
            if m:
                gcov.attribs['source.lines'] += 1
                gcov.attribs['source.lines.exec'] += 1
                exec_count = m.group (1)
                idx = m.group (2)
                gcov.newline (tmpl.TMPL_CODE_EXEC,
                        html.escape (m.group (3)), idx, exec_count)
                continue

            m = re_gcov_info.match (line)
            if m:
                gcov.newline (tmpl.TMPL_GCOV_INFO, html.escape (m.group (1)))
                continue

            if m is None: # pragma: no cover
                print ("parse:", src, "unkown line:", gcov_lines)

        fh.close ()

    gcov.status ()
    output.write_gcov_html (src, dst, gcov)

    return gcov
