#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import stat
import errno
import fuse
from json import loads, dumps
from fuse import Fuse
from plyvel import DB
from ast import literal_eval
from math import ceil


if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

db = DB('/home/cujo/nfs/db/db2')


class LWStat(fuse.Stat):
    def __init__(self):
        fuse.Stat.__init__(self)
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class LWFS(Fuse):
    def getattr(self, path):
        st = LWStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif db.get(b'i_' + bytes(path[1:])):
            st.st_mode = stat.S_IFREG | 0644
            st.st_nlink = 1
            st.st_size = int(loads(db.get(b'i_' + bytes(path[1:])))['f_size'])
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')
        for name, _ in db.iterator(prefix=b'i_'):
            yield fuse.Direntry(name[2:])

    def open(self, path, flags):
        return 0

    def fetch_contant(self, content_blocks):
        content = ''
        for block in content_blocks:
            if block:
                content += db.get(b'c_' + bytes(block))
        return content

    def fetch_content(self, content_blocks):
        content = ''
        for block in content_blocks:
            if block:
                content += db.get(b'c_' + bytes(block))
        return content

    def read(self, path, size, offset):
        content_blocks = loads(db.get(b'i_' + bytes(path[1:])))['f_blocks']
        content = self.fetch_contant(content_blocks)
        if not content:
            return -errno.ENOENT
        slen = len(content)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = content[offset:offset+size]
        else:
            buf = ''
        return buf

    def put_content(self, content, content_blocks, chunk_size):
        for i, block in enumerate(content_blocks):
            if block:
                db.put(b'c_' + bytes(block), content[i*chunk_size: (i+1)*chunk_size])

    def allocate_block(self):
        free_blocks = literal_eval(db.get(b'fb'))
        block = free_blocks.pop()
        db.put(b'fb', bytes(free_blocks))
        return block

    def write(self, path, buf, offset):
        xnode = loads(db.get(b'i_' + bytes(path[1:])))
        if xnode:
            block_size = loads(db.get(b'vfs'))['f_bsize']
            required_blocks = ceil(float(len(buf)) / block_size)
            if xnode['f_size'] == 0 or required_blocks > len(filter(None, xnode['f_blocks'])):
                for i in range(int(required_blocks)):
                    xnode['f_blocks'][xnode['f_blocks'].index(None)] = self.allocate_block()
            xnode['f_size'] = len(buf)
            self.put_content(buf, xnode['f_blocks'], block_size)
            db.put(b'i_' + bytes(path[1:]), dumps(xnode))
        else:
            return -errno.EPERM
        return len(buf)

    def statfs(self):
        return fuse.StatVfs(**loads(db.get(b'vfs')))

    def release(self, path, flags):
        return 0

    def truncate(self, path, size):
        return 0

    def utime(self, path, times):
        return 0


def main():
    usage = """ Userspace hello example""" + Fuse.fusage
    server = LWFS(version="%prog " + fuse.__version__, usage=usage)
    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
