from plyvel import DB
from json import dumps
from random import sample, randint


def update_vfs(new_block_size, new_blocks_count):
    db.put(b'vfs', dumps({b'f_bsize': new_block_size, b'f_frsize': new_block_size, b'f_blocks': total_blocks,
                          b'f_bfree': new_blocks_count, b'f_bavail': new_blocks_count}))


def save_free_blocks():
    inode0.f_frblocks = blocks_sample.pop()
    db.put(b'c_' + bytes(inode0.f_frblocks), bytes(blocks_sample))


def save_used_blocks():
    inode0.f_frblocks = blocks_sample.pop()
    used_blocks = list(set(sample(range(1, 8*block_size), 8*block_size - 1)) - set(blocks_sample))
    db.put(b'c_' + bytes(inode0.f_frblocks), bytes(used_blocks))


def put_inode(xnode):
    bytes_written = 0
    for k in range(randint(0, len(xnode.f_blocks))):
        block_number = blocks_sample.pop()
        xnode.f_blocks[k] = block_number
        bytes_written += populate_block(block_number)
    inode.f_size = bytes_written


def populate_block(number):
    db.put(b'c_' + str(number).encode(), data)
    return len(data)


def add_filename(filename):
    fnode = inode0.f_blocks[inode0.f_size / block_size]
    namepair = bytes((filename, i))
    if fnode:
        current_content = db.get(b'c_' + bytes(fnode))
        if len(current_content) + len(namepair) > block_size:
            db.put(b'c_' + bytes(fnode), db.get(b'c_' + bytes(fnode)) + namepair[:block_size - len(current_content)])
            allocate_block = blocks_sample.pop()
            inode0.f_blocks[inode0.f_blocks.index(None)] = allocate_block
            db.put(b'c_' + bytes(allocate_block), namepair[block_size - len(current_content):])
        else:
            db.put(b'c_' + bytes(fnode), db.get(b'c_' + bytes(fnode)) + namepair)
    else:
        allocate_block = blocks_sample.pop()
        inode0.f_blocks[inode0.f_blocks.index(None)] = allocate_block
        db.put(b'c_' + bytes(allocate_block), namepair)
    inode0.f_size = inode0.f_size + len(namepair)
    

# Random String Data to put into a single block of size 1024.
data = b'JBwYcVOxKchXnaLmwEYfKtHwkwSKKgOpVGPPDgyKjvPnFlpLZPbTPSrOot\ntIMPTQ' \
       b'GNBor\nFZyFAYsPnFopzqlhBnJNSrHEnqrLpdSsfWAvKeuX\nclNERw\nzVyguZLGt' \
       b'bMnGcyfbFIkYmygITbcwvHkIgVabTLHTJWlfzJPMNOguOdnxOLJsLGluLdOkpYfmPg' \
       b'IQuUMiQVFNLTQmaIaNKsbGQxFWrywmestAJZXkOJZIqIcMcjknPaamHIqMMwtqTxPu' \
       b'Wvm\nZTMJFhOZVLxVXTOGCEfegcep\nGTppyVwnAgIVEdiERUGrkqGympBXJWEIFsi' \
       b'gbWSotaHcKX\nAsDEOfWMfzTaBjgQjpBrYwzlgj\nLFWswqcVDMglAEYhCBbqfERMk' \
       b'yEkysRxw\nRn\nNWcKScMIGPsBlhvGbKVlLWeBODIhZgHlZzjAXVhsuEEaUCvafROW' \
       b'hdedfiXDhQuP\niCpmwKI\nRcwZqHngBdQYwCPf\nLaSSRoZdrmiiNYtLgjKRJuFeY' \
       b'vNv\nMPiGYcLHOKeL\n\ndyNSQWVwTfKjDcjzOvPhVeFLMzpielMe\nDze\nPTJZBn' \
       b'BUbfOcFiFeoPcGqMUpCKUUNu\nql\njTAdw\nTt\niAfDOSOMSC\nAqZZvytuJ\nCd' \
       b'wXrNWnjH\nEIjWywukTxAjQfihOGLItawpcSAbOSLwsBfvWMKxqFxiBJNYCWlhsHnZ' \
       b'NLjvORg\n\nYdNLygoIguOxdhfGKrZVnRLGlUGlWZBqonCcDxfITfrVukEyCLYjOFR' \
       b'IJgQy\n\nIvwPOSLuBQwONyhgLOu\nNxL\nMnuxVByFuHOUJ\nZyhMOngsejbZ\nJL' \
       b'Rjo\nCYYGqssFJNyjIOIOYCkdTZMypLqSGkeXXoEmErcxvaDQCTcTEYbZOUWngLYpM' \
       b'fJqZZO\nQNDHS\nQSmDllrK\nsiAgAAmIfyWhyNWpRLAyKhVEnI\nSkPLGkZZNrgJo' \
       b'YMWOFudgegHBEOwufZfOUAMmzrqCEEGozQPPnLXhZcFyNQpnOTnmfPKsMVcndWtOUr' \
       b'WwqYN\n'

# Random filenames
file_names = [
'4sz', 'mqx', '1gg', '76c', '4nb', '5g7', 'u8w', 'kn4', 'dgb', '4tw', 'vaf',
'u6s', '9br', 'cub', 'eec', '4ke', '8ef', 'sbb', '6i5', 'ao4', 'lyn', 'ns6',
'gsx', 'ski', 'x15', 'ok4', '8rt', '7iv', 'tbo', 'd6m', 'snt', '2o5', 'mrp',
'4sz', 'mqx', '1gg', '76c', '4nb', '5g7', 'u8w', 'kn4', 'dgb', '4tw', 'vaf',
'u6s', '9br', 'cub', 'eec', '4ke', '8ef', 'sbb', '6i5', 'ao4', 'lyn', 'ns6',
]


class INode(object):
    def __init__(self):
        self.f_size = int(0)
        self.f_blocks = [None] * 8
        # Free blocks - Can be ignored
        self.f_frblocks = int(0)


# Special INode to keep tarck of the root directory.
# In this case, it will take care of inode to filenames mapping, id of free inodes
inode0 = INode()
total_blocks = 1024*10
block_size = 1024

# Random unique block numbers on which data will reside
blocks_sample = sample(range(1, 8*block_size), 8*block_size - 1)
db = DB('/home/cujo/nfs/db/db3', create_if_missing=True)

for i in range(len(file_names)):
    inode = INode()
    put_inode(inode)
    add_filename(file_names[i])
    db.put(b'i_' + str(i).encode(), dumps(inode.__dict__))


# Keeping track of unused blocks
# save_free_blocks()
save_used_blocks()
# Finally saving INode0
db.put(b'i_0', dumps(inode0.__dict__))
# Updating FS status
update_vfs(block_size, total_blocks - (8*block_size - len(blocks_sample)) - len(file_names) - 1)

db.close()

# Some Stats collection for evaluation
print('Total Blocks inserted = ' + str(total_blocks - (8*block_size - len(blocks_sample)) - len(file_names) - 1))
