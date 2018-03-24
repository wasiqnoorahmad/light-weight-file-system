import plyvel
import json

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

file_names = ['epw', 'gmf', 'qmj', 'oyg', 'gxs', 'vdl', 'mpi', 'utb', 'dgq', 'xnw', 'lfu',
              'lqb', 'jhu', 'vyv', 'aql', 'tkd', 'ezl', 'qpf', 'gmo', 'ajy', 'iwe', 'boq',
              'huq', 'egl', 'vad', 'igj', 'emm', 'tjd', 'dri', 'yfq', 'xxr', 'zrw', 'zrn',
              'thk', 'kax', 'dfo', 'ctn', 'pyq', 'hzs', 'ndf']

blocks = 50
block_size = 1024
db = plyvel.DB('/home/cujo/nfs/db/db1', create_if_missing=True)
db.delete(b'vfs')
db.put(b'vfs', json.dumps({b'f_bsize': block_size, b'f_frsize': block_size, b'f_blocks': blocks,
                           b'f_bfree': blocks, b'f_bavail': blocks}))
for index, file_name in enumerate(file_names):
    db.delete(b'f_' + file_name.encode())
    db.put(b'f_' + file_name.encode(), data)
    db.put(b'vfs', json.dumps({b'f_bsize': block_size, b'f_frsize': block_size, b'f_blocks': blocks,
                               b'f_bfree': blocks-(index + 1), b'f_bavail': blocks-(index + 1)}))
db.close()
