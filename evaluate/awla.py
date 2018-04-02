def convert_size_to_bytes(size):
    size = size.replace(' ', '')
    multipliers = {
        'kb': 1024,
        'mb': 1024*1024,
        'gb': 1024*1024*1024,
        'tb': 1024*1024*1024*1024
    }

    for suffix in multipliers:
        if size.lower().endswith(suffix):
            return float(size[0:-len(suffix)]) * multipliers[suffix]
    else:
        if size.lower().endswith('b'):
            return float(size[0:-1])

    try:
        return float(size)
    except ValueError: # for example "1024x"
        print('Malformed input!')
        exit()

print(convert_size_to_bytes('1.1MB'))
