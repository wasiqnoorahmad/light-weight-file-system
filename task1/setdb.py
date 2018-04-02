import plyvel
import json
import sys

data = b'JBwYcVOxKchXnaLmwEYfKtHwkwSKKgOpVGPPDgyKjvPnFlpLZPbTPSrOot\ntIMPTQ' \
       b'GNBor\nFZyFAYsPnFopzqlhBnJNSrHEnqrLpdSsfWAvKeuX\nclNERw\nzVyguZLGt' \
       b'bMnGcyfbFIkYmygITbcwvHkIgVabTLHTJWlfzJPMNOguOdnxOLJsLGluLdOkpYfmPg' \
       b'IQuUMiQVFNLTQmaIaNKsbGQxFWrywmestAJZXkOJZIqIcMcjknPaamHIqMMwtqTxPu' \
       b'Wvm\nZTMJFhOZVLxVXTOGCEfegcep\nGTppyVwnAgIVEdiERUGrkqGympBXJWEIFsi' \
       b'gbWSotaHcKX\nAsDEOfWMfzTaBjgQjpBrYwzlgj\nLFWswqcVDMglAEYhCBbqfERMk' \
       b'yEkysRxw\nRn\nNWcKScMIGPsBlhvGbKVlLWeBODIhZgHlZzjAXVhsuEEaUCvafROW'

# file_names = ['in', 'gmf', 'qmj', 'oyg', 'gxs', 'vdl', 'mpi', 'utb', 'dgq', 'xnw', 'lfu',
#               'lqb', 'jhu', 'vyv', 'aql', 'tkd', 'ezl', 'qpf', 'gmo', 'ajy', 'iwe', 'boq',
#               'huq', 'egl', 'vad', 'igj', 'emm', 'tjd', 'dri', 'yfq', 'xxr', 'zrw', 'zrn',
#               'thk', 'kax', 'dfo', 'ctn', 'pyq', 'hzs', 'out']

blocks = 50
block_size = 1024
db = plyvel.DB('/home/cujo/nfs/db/db1', create_if_missing=True, block_size=int(sys.argv[1]))
db.delete(b'vfs')
db.put(b'vfs', json.dumps({b'f_bsize': block_size, b'f_frsize': block_size, b'f_blocks': blocks,
                           b'f_bfree': blocks, b'f_bavail': blocks}))
for index in range(20):
    db.delete(b'f_' + bytes(index))
    if index == 1:
        db.put(b'f_' + bytes(index), ' ')
    else:
        db.put(b'f_' + bytes(index), data)
    db.put(b'vfs', json.dumps({b'f_bsize': block_size, b'f_frsize': block_size, b'f_blocks': blocks,
                               b'f_bfree': blocks-(index + 1), b'f_bavail': blocks-(index + 1)}))
db.close()
