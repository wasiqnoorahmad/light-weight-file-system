#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, stat, errno
import fuse
from ast import literal_eval
from json import loads, dumps
from fuse import Fuse
from plyvel import DB
from random import sample
from math import ceil


if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

db = DB('/home/cujo/nfs/db/db3')


class LWStat(fuse.Stat):
    def __init__(self):
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


class INode(object):
    def __init__(self):
        self.f_size = int(0)
        self.f_blocks = [None] * 8
        self.f_frblocks = int(0)


class LWFS(Fuse):
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)
        self.files = {}

        # Loading Files to INode Mapping
        blocks = loads(db.get(b'i_0'))[b'f_blocks']
        buff = self.fetch_content(blocks).replace(')', '),')
        self.files = dict(literal_eval(buff))

    def update_filenames(self):
        block_size = loads(db.get(b'vfs'))['f_bsize']
        self.put_content(bytes(self.files.items()).replace('),', ')').replace('[', '').replace(']', ''),
                         loads(db.get(b'i_0'))[b'f_blocks'], block_size)

    def fetch_content(self, content_blocks):
        content = ''
        for block in content_blocks:
            if block:
                content += db.get(b'c_' + bytes(block))
        return content

    def put_content(self, content, content_blocks, chunk_size):
        for i, block in enumerate(content_blocks):
            if block:
                db.put(b'c_' + bytes(block), content[i*chunk_size: (i+1)*chunk_size])

    def getattr(self, path):
        st = LWStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path[1:] in self.files:
            inode_number = b'i_' + bytes(self.files[path[1:]])
            st.st_mode = stat.S_IFREG | 0664
            st.st_nlink = 1
            st.st_size = loads(db.get(inode_number))['f_size']
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')
        for name in self.files.keys():
            yield fuse.Direntry(name)

    def open(self, path, flags):
        return 0

    def fsync(self, path, isfsyncfile):
        return 0

    def read(self, path, size, offset):
        inode_number = b'i_' + bytes(self.files[path[1:]])
        content_blocks = loads(db.get(inode_number))['f_blocks']
        content = self.fetch_content(content_blocks)
        slen = len(content)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = content[offset:offset+size]
        else:
            buf = ''
        return buf

    def statfs(self):
        return fuse.StatVfs(**loads(db.get(b'vfs')))

    def update_vfs(self, new_block_size, new_blocks_count, total_blocks):
        db.put(b'vfs', dumps({b'f_bsize': new_block_size, b'f_frsize': new_block_size, b'f_blocks': total_blocks,
                              b'f_bfree': new_blocks_count, b'f_bavail': new_blocks_count}))

    def allocate_block(self):
        vfs = loads(db.get(b'vfs'))
        block_size = vfs['f_bsize']
        total_blocks = vfs[b'f_blocks']
        blocks_sample = sample(range(1, 8 * block_size), 8 * block_size - 1)
        used_blocks_block_number = loads(db.get(b'i_0'))[b'f_frblocks']
        used_blocks = literal_eval(db.get(b'c_' + bytes(used_blocks_block_number)))
        free_blocks = list(set(blocks_sample) - set(used_blocks))
        block = free_blocks.pop()
        used_blocks.append(block)
        self.put_content(bytes(used_blocks), [used_blocks_block_number], len(bytes(used_blocks)))
        self.update_vfs(block_size, vfs['f_bavail'] - 1, total_blocks)
        return block

    def unlink(self, path):
        inode_number = b'i_' + bytes(self.files[path[1:]])
        self.files.pop(path[1:], None)
        # Blocks freed after the deletion of this file
        free_blocks = loads(db.get(inode_number))['f_blocks']
        # free_blocks now needs to be removed from the used blocks in lvldb, because they
        # are no more used now
        used_blocks_block_number = loads(db.get(b'i_0'))[b'f_frblocks']
        used_blocks = literal_eval(db.get(b'c_' + bytes(used_blocks_block_number)))
        for free_block in free_blocks:
            if free_block:
                used_blocks.remove(free_block)
        print()
        db.put(b'c_' + bytes(used_blocks_block_number), bytes(used_blocks))
        self.update_filenames()
        db.delete(inode_number)

    def write(self, path, buf, offset):
        print('In write')
        # print('Buf', buf)
        # xnode= INode()
        # xnode_id = self.allocate_block()
        # buffer_size = loads(db.get(b'vfs'))['f_bsize']
        # print('Length of content is: ', len(buf))
        # print('And content is, ', buf)
        # required_blocks = ceil(float(len(buf)) / loads(db.get(b'vfs'))['f_bsize'])
        # print("Required Blocks are: ", required_blocks)
        # for i in range(int(required_blocks)):
        #     xnode.f_blocks[i] = self.allocate_block()
        # self.put_content(buf, xnode.f_blocks, buffer_size)
        # self.files[path[1:]] = bytes(xnode_id)
        # self.update_filenames()
        # db.put(b'i_' + bytes(xnode_id), dumps(xnode.__dict__))
        # print('Block is ', db.get(b'i_' + bytes(xnode_id)))
        # print('In write')
        return len(buf)
        # print(path, buf, offset)
        # return 12
        # # inode = db.get(b'i_' + path[1:].encode())

    def mknod(self, path, mode, dev):
        xnode = INode()
        xnode_id = self.allocate_block()
        self.files[path[1:]] = bytes(xnode_id)
        self.update_filenames()
        db.put(b'i_' + bytes(xnode_id), dumps(xnode.__dict__))
        return 0

    def rename(self, pathfrom, pathto):
        if pathfrom[1:] in self.files:
            self.files[pathto[1:]] = self.files.pop(pathfrom[1:])
            self.update_filenames()
        else:
            return -errno.ENOENT
        return 0

    def release(self, path, flags):
        print("In release")
        # print(path)

    def truncate(self, path, size):
        return 0

    def utime(self, path, times):
        return 0


def main():
    usage = """ Userspace hello example""" + Fuse.fusage
    server = LWFS(version="%prog " + fuse.__version__, usage=usage, dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()


if __name__ == '__main__':
    main()
