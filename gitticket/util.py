# -*- coding:utf-8 -*-

import subprocess as sp
import tempfile
import re


def strwidth(s):
    return sum(1 if ord(x) < 256 else 2 for x in s)


def cmd_stdout(arglist):
    return sp.Popen(arglist, stdout=sp.PIPE).communicate()[0].strip()


def rmcomment(text):
    u"""空行はそのまま、コメントのみの行は行ごと削除する
    """
    r = []
    for line in text.split(u'\n'):
        l = line.split('#', 1)[0]
        # 最初から空行、またはコメント削除後に文字があったら追加
        if l or not line:
            r.append(l)
    return u'\n'.join(r)


def regex_extract(pattern, tgt, default=None):
    r = re.search(pattern, tgt, re.M | re.S)
    if not r:
        return default
    grps = r.groups()
    if len(grps) == 1:
        return grps[0]
    return grps


def inputwitheditor(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    editor = cmd_stdout(('git', 'var', 'GIT_EDITOR')).split(u' ')
    tmpfile = tempfile.mkstemp()
    with open(tmpfile[1], 'w') as fo:
        fo.write(s)
    cmd_stdout(editor + [tmpfile[1]])
    
    return open(tmpfile[1]).read()

