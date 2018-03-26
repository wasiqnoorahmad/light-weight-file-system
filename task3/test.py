from plyvel import DB
from json import loads
from random import sample
from ast import literal_eval
from json import dumps
from random import randint

db = DB('/home/cujo/nfs/db/db3')


def put_content(content, content_blocks, chunk_size):
    for i, block in enumerate(content_blocks):
        if block:
            db.put(b'c_' + bytes(block), content[i * chunk_size: (i + 1) * chunk_size])


def update_vfs(new_block_size, new_blocks_count, total_blocks):
    db.put(b'vfs', dumps({b'f_bsize': new_block_size, b'f_frsize': new_block_size, b'f_blocks': total_blocks,
                          b'f_bfree': new_blocks_count, b'f_bavail': new_blocks_count}))

def allocate_block():
    vfs = loads(db.get(b'vfs'))
    block_size = vfs['f_bsize']
    total_blocks = vfs[b'f_blocks']
    blocks_sample = sample(range(1, 8 * block_size), 8 * block_size - 1)
    used_blocks_block_number = loads(db.get(b'i_0'))[b'f_frblocks']
    used_blocks = literal_eval(db.get(b'c_' + bytes(used_blocks_block_number)))
    free_blocks = list(set(blocks_sample) - set(used_blocks))
    block = free_blocks.pop()
    used_blocks.append(block)
    put_content(bytes(used_blocks), [used_blocks_block_number], len(bytes(used_blocks)))
    update_vfs(block_size, vfs['f_bavail'] - 1, total_blocks)
    return block


def put_inode(xnode):
    bytes_written = 0
    for k in range(randint(0, len(xnode.f_blocks))):
        block_number = allocate_block()
        xnode.f_blocks[k] = block_number
        # bytes_written += populate_block(block_number)
    xnode.f_size = bytes_written

    db.put(b'i_' + str(i).encode(), dumps(inode.__dict__))

def allocate_inode():
    pass
    # vfs = loads(db.get(b'vfs'))
    # block_size = vfs['f_bsize']
    # total_blocks = vfs[b'f_blocks']
    # blocks_sample = sample(range(1, 8 * block_size), 8 * block_size - 1)
    # used_blocks_block_number = loads(db.get(b'i_0'))[b'f_frblocks']
    # used_blocks = literal_eval(db.get(b'c_' + bytes(used_blocks_block_number)))
    # free_blocks = list(set(blocks_sample) - set(used_blocks))
    # block = free_blocks.pop()
    # used_blocks.append(block)
    # put_content(bytes(used_blocks), [used_blocks_block_number], len(bytes(used_blocks)))
    # update_vfs(block_size, vfs['f_bavail'] - 1, total_blocks)
    # return block


# used_blocks_block_number = loads(db.get(b'i_0'))[b'f_frblocks']
# used_blocks = literal_eval(db.get(b'c_' + bytes(used_blocks_block_number)))
# print(used_blocks)
print(db.get(b'vfs'))
allocate_block()
# allocate_block()
print(db.get(b'vfs'))
# # print(db.get(b'c_' + bytes(loads(db.get(b'i_0'))[b'f_frblocks'])))
# # print(len(db.get(b'c_' + bytes(loads(db.get(b'i_0'))[b'f_frblocks']))))