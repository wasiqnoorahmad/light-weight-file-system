from plyvel import DB
from json import dumps
from random import sample


def update_vfs(new_block_size, new_blocks_count):
    db.put(b'vfs', dumps({b'f_bsize': new_block_size, b'f_frsize': new_block_size, b'f_blocks': total_blocks,
                          b'f_bfree': new_blocks_count, b'f_bavail': new_blocks_count}))
    return new_block_size, new_blocks_count - 1


def populate_block(number):
    db.put(b'c_' + str(number).encode(), data)
    return len(data)


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
# Random unique block numbers on which data will reside
blocks_sample = iter(sample(range(0, 8*1024), 8*1024))


class INode(object):
    def __init__(self):
        self.f_size = int(0)
        self.f_blocks = [None] * 8
        # Free blocks - Can be ignored
        self.f_frblocks = int(0)


total_blocks = 1024*10
block_size = 1024
ev_inodes, ev_blocks = (0, 0)
db = DB('/home/cujo/nfs/db/db2', create_if_missing=True)
_, current_blocks = update_vfs(block_size, total_blocks)


for i in range(1024):
    bytes_written = 0
    inode = INode()
    for k in range(len(inode.f_blocks)):
        block_number = next(blocks_sample)
        inode.f_blocks[k] = block_number
        bytes_written += populate_block(block_number)
        ev_blocks += 1
        _, current_blocks = update_vfs(block_size, current_blocks)
    inode.f_size = bytes_written
    db.put(b'i_' + str(i).encode(), dumps(inode.__dict__))
    ev_inodes += 1
    _, current_blocks = update_vfs(block_size, current_blocks)
db.close()

# Some Stats collection for evaluation
print('Total Blocks inserted = ', ev_blocks)
print('Total INodes inserted = ', ev_inodes)
