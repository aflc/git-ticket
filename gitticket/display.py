#!/usr/bin/env python
# -*- coding:utf-8 -*-

import blessings
from gitticket import util

class Table(object):
    def __init__(self, tickets):
        self.colcfg = []
        self.tickets = tickets
        self.margin = 2
        self.reducename = None
    
    def addcolumn(self, kwargs):
        self.colcfg.append(kwargs)

    def fit(self):
        for col in self.colcfg:
            col['width'] = max(util.strwidth(x[col['name']]) for x in self.tickets)
            col['width'] = max(col['width'], util.strwidth(col['name']))
        if self.reducename:
            totwidth = sum(x['width'] for x in self.colcfg)
            deltawidth = totwidth - termwidth()
            if deltawidth > 0:
                self.colcfg[self.reducename]['width'] = max(self.colcfg[self.reducename]['width'] - deltawidth, util.strwidth(self.reducename))
        
    def output(self):
        lines = [[], []]
        for col in self.colcfg:
            gluelen = col['width'] - util.strwidth(col['name'])
            lines[0].append(col['name'] + u' ' * gluelen)
            lines[1].append(u'-' * (len(col['name']) + gluelen))
        for ticket in self.tickets:
            lines.append([ticket.tostr(x['name'], x['width']) for x in self.colcfg])
        return u'\n'.join((u' ' * self.margin).join(x) for x in lines)


def ticketlist(tickets):
    u"""Ticketオブジェクトのリストを表示する"""
    t = Table(tickets)
    for name in ('id', 'title', 'assign', 'c', 'create', 'update'):
        if all(getattr(x, name, None) is not None for x in tickets):
            t.addcolumn({'name':name})
    t.reducename = 'title'
    t.fit()
    return t.output()
            
def ticketdetail(tic):
    r = u'\n'
    r += u'[{state}] #{id} {title}\n'.format(state=tic.state, id=tic.id, title=tic.title)
    r += horline() + u'\n'
    r += u'By {created_by} {create} with {commentnum} comments\n'.format(created_by=tic.created_by, create=tic.create, commentnum=tic.c)
    r += u'Updated at: {update}\n'.format(update=tic.update)
    if tic.labels:
        r += u'Labels: {labels}\n'.format(labels=u', '.join(tic.labels))
    r += '\n'
    r += tic.body
    
    return r


def termwidth():
    term = blessings.Terminal()
    return term.width


def horline(linestr=u'-'):
    return linestr * termwidth()
